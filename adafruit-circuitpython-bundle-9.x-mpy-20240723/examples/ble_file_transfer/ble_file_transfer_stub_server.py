# SPDX-FileCopyrightText: Copyright (c) 2021 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""This example broadcasts out the creation id based on the CircuitPython machine
   string and provides a stub FileTransferService."""

import binascii
import struct
import os
import time

import adafruit_ble
import adafruit_ble_creation

import adafruit_ble_file_transfer
from adafruit_ble_file_transfer import FileTransferService

cid = adafruit_ble_creation.creation_ids[os.uname().machine]

ble = adafruit_ble.BLERadio()
# ble._adapter.erase_bonding()

service = FileTransferService()
print(ble.name)
advert = adafruit_ble_creation.Creation(creation_id=cid, services=[service])
print(binascii.hexlify(bytes(advert)), len(bytes(advert)))

CHUNK_SIZE = 4000

stored_data = {}
# path to timestamp, no nesting
stored_timestamps = {}


def find_dir(full_path):
    parts = full_path.split("/")
    parent_dir = stored_data
    k = 1
    while k < len(parts) - 1:
        part = parts[k]
        if part not in parent_dir:
            return None
        parent_dir = parent_dir[part]
        k += 1
    return parent_dir


def read_packets(buf, *, target_size=None):
    if not target_size:
        target_size = len(buf)
    total_read = 0
    buf = memoryview(buf)
    while total_read < target_size:
        count = service.raw.readinto(buf[total_read:])
        total_read += count

    return total_read


def write_packets(buf):
    packet_length = service.raw.outgoing_packet_length
    if len(buf) <= packet_length:
        service.raw.write(buf)
        return

    full_packet = memoryview(bytearray(packet_length))
    sent = 0
    while offset < len(buf):
        this_packet = full_packet[: len(buf) - sent]
        for k in range(len(this_packet)):  # pylint: disable=consider-using-enumerate
            this_packet[k] = buf[sent + k]
        sent += len(this_packet)
        service.raw.write(this_packet)


def read_complete_path(starting_path, total_length):
    complete_path = bytearray(total_length)
    current_path_length = len(starting_path)
    remaining_path = total_length - current_path_length
    complete_path[:current_path_length] = starting_path
    if remaining_path > 0:
        read_packets(
            memoryview(complete_path)[current_path_length:], target_size=remaining_path
        )
    return str(complete_path, "utf-8")


packet_buffer = bytearray(CHUNK_SIZE + 20)
# Mimic the disconnections that happen when a CP device reloads and resets BLE.
disconnect_after = None
while True:
    ble.start_advertising(advert)
    while not ble.connected:
        pass
    print("connected")
    while ble.connected:
        try:
            read = service.raw.readinto(packet_buffer)
        except ConnectionError:
            continue
        if disconnect_after is not None and time.monotonic() > disconnect_after:
            for c in ble.connections:
                c.disconnect()
            disconnect_after = None
            continue
        if read == 0:
            continue

        p = packet_buffer[:read]
        command = struct.unpack_from("<B", p)[0]
        if command == FileTransferService.WRITE:
            (
                path_length,
                start_offset,
                modification_time,
                content_length,
            ) = struct.unpack_from("<xHIQI", p, offset=1)
            path_start = struct.calcsize("<BxHIQI")
            path = read_complete_path(p[path_start:], path_length)

            d = find_dir(path)
            filename = path.rsplit("/", maxsplit=1)[-1]
            if filename not in d:
                contents = bytearray(content_length)
                d[filename] = contents
            current_len = len(d[filename])
            if current_len < content_length:
                contents = d[filename] + bytearray(content_length - current_len)
            elif current_len > content_length:
                contents = d[filename][:content_length]
            else:
                contents = d[filename]
            d[filename] = contents
            contents_read = start_offset
            write_data_header_size = struct.calcsize("<BBxxII")
            data_size = 0
            ok = True

            # Trucate to the nearest 3 seconds.
            truncation = 3 * 1_000_000_000
            truncated_time = (modification_time // truncation) * truncation

            while contents_read < content_length and ok:
                next_amount = min(CHUNK_SIZE, content_length - contents_read)
                header = struct.pack(
                    "<BBxxIQI",
                    FileTransferService.WRITE_PACING,
                    FileTransferService.OK,
                    contents_read,
                    truncated_time,
                    next_amount,
                )
                write_packets(header)
                read = read_packets(
                    packet_buffer, target_size=next_amount + write_data_header_size
                )
                cmd, status, offset, data_size = struct.unpack_from(
                    "<BBxxII", packet_buffer
                )
                if status != FileTransferService.OK:
                    print("bad status, resetting")
                    ok = False
                if cmd != FileTransferService.WRITE_DATA:
                    write_packets(
                        struct.pack(
                            "<BBxxIQI",
                            FileTransferService.WRITE_PACING,
                            FileTransferService.ERROR_PROTOCOL,
                            0,
                            truncated_time,
                            0,
                        )
                    )
                    print("protocol error, resetting")
                    ok = False

                contents[contents_read : contents_read + data_size] = packet_buffer[
                    write_data_header_size : write_data_header_size + data_size
                ]
                contents_read += data_size
            if not ok:
                break

            stored_timestamps[path] = truncated_time
            disconnect_after = time.monotonic() + 0.7
            write_packets(
                struct.pack(
                    "<BBxxIQI",
                    FileTransferService.WRITE_PACING,
                    FileTransferService.OK,
                    content_length,
                    truncated_time,
                    0,
                )
            )
        elif command == adafruit_ble_file_transfer.FileTransferService.READ:
            path_length, offset, free_space = struct.unpack_from("<xHII", p, offset=1)
            path_start = struct.calcsize("<BxHII")
            path = read_complete_path(p[path_start:], path_length)
            d = find_dir(path)
            filename = path.rsplit("/", maxsplit=1)[-1]
            if d is None or filename not in d:
                print("missing path")
                error_response = struct.pack(
                    "<BBxxIII",
                    FileTransferService.READ_DATA,
                    FileTransferService.ERR,
                    0,
                    0,
                    0,
                )
                write_packets(error_response)
                continue

            contents_sent = offset
            contents = d[filename]
            while contents_sent < len(contents):
                remaining = len(contents) - contents_sent
                next_amount = min(remaining, free_space)
                header = struct.pack(
                    "<BBxxIII",
                    FileTransferService.READ_DATA,
                    FileTransferService.OK,
                    contents_sent,
                    len(contents),
                    next_amount,
                )
                write_packets(
                    header + contents[contents_sent : contents_sent + next_amount]
                )
                contents_sent += next_amount

                if contents_sent == len(contents):
                    break

                read = read_packets(
                    packet_buffer, target_size=struct.calcsize("<BBxxII")
                )
                cmd, status, offset, free_space = struct.unpack_from(
                    "<BBxxII", packet_buffer
                )
                if cmd != FileTransferService.READ_PACING:
                    write_packets(
                        struct.pack(
                            "<BBxxIII",
                            FileTransferService.READ_DATA,
                            FileTransferService.ERROR_PROTOCOL,
                            0,
                            0,
                            0,
                        )
                    )
                    print("protocol error", packet_buffer[:10])
                    break
                if offset != contents_sent:
                    write_packets(
                        struct.pack(
                            "<BBxxIII",
                            FileTransferService.READ_DATA,
                            FileTransferService.ERROR_PROTOCOL,
                            0,
                            0,
                            0,
                        )
                    )
                    print("mismatched offset")
                    break
        elif command == adafruit_ble_file_transfer.FileTransferService.MKDIR:
            path_length, modification_time = struct.unpack_from("<xHxxxxQ", p, offset=1)
            # Trucate to the nearest 3 seconds.
            truncation = 3 * 1_000_000_000
            truncated_time = (modification_time // truncation) * truncation
            path_start = struct.calcsize("<BxHxxxxQ")
            path = read_complete_path(p[path_start:], path_length)
            pieces = path.split("/")[1:-1]
            parent = stored_data
            i = 0
            ok = True
            while i < len(pieces) and ok:
                piece = pieces[i]
                if piece not in parent:
                    parent[piece] = {}
                elif not isinstance(parent[piece], dict):
                    ok = False
                parent = parent[piece]
                i += 1

            if ok:
                header = struct.pack(
                    "<BBxxxxxxQ",
                    FileTransferService.MKDIR_STATUS,
                    FileTransferService.OK,
                    truncated_time,
                )
                stored_timestamps[path] = truncated_time
            else:
                header = struct.pack(
                    "<BBxxxxxxQ",
                    FileTransferService.MKDIR_STATUS,
                    FileTransferService.ERR,
                    0,
                )
            write_packets(header)
        elif command == adafruit_ble_file_transfer.FileTransferService.LISTDIR:
            path_length = struct.unpack_from("<xH", p, offset=1)[0]
            path_start = struct.calcsize("<BxH")
            path = read_complete_path(p[path_start:], path_length)

            # cmd, status, i, total, flags, file_size, path_length = struct.unpack("<BBIIBIH", b)

            d = find_dir(path)
            if d is None:
                error = struct.pack(
                    "<BBHIIIQI",
                    FileTransferService.LISTDIR_ENTRY,
                    FileTransferService.ERROR,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                )
                write_packets(error)
                continue

            filenames = sorted(d.keys())
            total_files = len(filenames)
            for i, filename in enumerate(filenames):
                encoded_filename = filename.encode("utf-8")
                flags = 0
                contents = d[filename]
                if isinstance(contents, dict):
                    flags = FileTransferService.DIRECTORY
                    content_length = 0
                else:
                    content_length = len(contents)
                full_file_path = path + filename
                if flags == FileTransferService.DIRECTORY:
                    full_file_path += "/"
                timestamp = stored_timestamps[full_file_path]
                header = struct.pack(
                    "<BBHIIIQI",
                    FileTransferService.LISTDIR_ENTRY,
                    FileTransferService.OK,
                    len(encoded_filename),
                    i,
                    total_files,
                    flags,
                    timestamp,
                    content_length,
                )
                packet = header + encoded_filename
                write_packets(packet)

            header = struct.pack(
                "<BBHIIIQI",
                FileTransferService.LISTDIR_ENTRY,
                FileTransferService.OK,
                0,
                total_files,
                total_files,
                0,
                0,
                0,
            )
            write_packets(header)
        elif command == adafruit_ble_file_transfer.FileTransferService.DELETE:
            path_length = struct.unpack_from("<xH", p, offset=1)[0]
            path_start = struct.calcsize("<BxH")
            path = read_complete_path(p[path_start:], path_length)
            d = find_dir(path)
            filename = path.rsplit("/", maxsplit=1)[-1]

            # We're a directory.
            if not filename and d is not None:
                filename = path[:-1].rsplit("/", maxsplit=1)[-1]
                d = find_dir(path[:-1])

            if d is None or filename not in d or path == "/":
                print("missing path", path, d)
                error_response = struct.pack(
                    "<BB", FileTransferService.DELETE_STATUS, FileTransferService.ERROR
                )
                write_packets(error_response)
                continue
            ok = True

            del stored_timestamps[path]
            del d[filename]

            header = struct.pack(
                "<BB", FileTransferService.DELETE_STATUS, FileTransferService.OK
            )
            write_packets(header)
        elif command == adafruit_ble_file_transfer.FileTransferService.MOVE:
            old_path_length, new_path_length = struct.unpack_from("<xHH", p, offset=1)
            path_start = struct.calcsize("<BxHH")
            # We read in one extra character and then discard it. We don't need it. (C does.)
            both_paths = read_complete_path(
                p[path_start:], old_path_length + 1 + new_path_length
            )
            old_path = both_paths[:old_path_length]
            new_path = both_paths[old_path_length + 1 :]

            old_d = find_dir(old_path)
            old_filename = old_path.split("/")[-1]
            # If we're a directory then move up one.
            if not old_filename and old_d is not None:
                old_filename = old_path[:-1].split("/")[-1]
                old_d = find_dir(old_path[:-1])

            new_d = find_dir(new_path)
            new_filename = new_path.split("/")[-1]
            # If we're a directory then move up one.
            if not new_filename and new_d is not None:
                new_filename = new_path[:-1].split("/")[-1]
                new_d = find_dir(new_path[:-1])

            if old_d is None or old_filename not in old_d or old_path == "/":
                print("missing old path", old_path)
                error_response = struct.pack(
                    "<BB", FileTransferService.MOVE_STATUS, FileTransferService.ERROR
                )
                write_packets(error_response)
                continue

            if new_d is None or new_filename in new_d or new_path == "/":
                print("missing new path", new_path)
                error_response = struct.pack(
                    "<BB", FileTransferService.MOVE_STATUS, FileTransferService.ERROR
                )
                write_packets(error_response)
                continue

            new_d[new_filename] = old_d[old_filename]
            del old_d[old_filename]
            stored_timestamps[new_path] = stored_timestamps[old_path]
            del stored_timestamps[old_path]

            header = struct.pack(
                "<BB", FileTransferService.MOVE_STATUS, FileTransferService.OK
            )
            write_packets(header)
        else:
            print("unknown command", hex(command))
    print("disconnected - ", end="")
