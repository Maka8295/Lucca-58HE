# SPDX-FileCopyrightText: 2024 Justin Myers for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import os
import time

import adafruit_connection_manager

try:
    import wifi

    radio = wifi.radio
    onboard_wifi = True
except ImportError:
    import board
    import busio
    from adafruit_esp32spi import adafruit_esp32spi
    from digitalio import DigitalInOut

    # esp32spi pins set based on Adafruit AirLift FeatherWing
    # if using a different setup, please change appropriately
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    esp32_cs = DigitalInOut(board.D13)
    esp32_ready = DigitalInOut(board.D11)
    esp32_reset = DigitalInOut(board.D12)
    radio = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
    onboard_wifi = False


# built from:
#  https://github.com/adafruit/Adafruit_Learning_System_Guides
ADAFRUIT_GROUPS = [
    {
        "heading": "API hosts",
        "description": "These are common API hosts users hit.",
        "success": "yes",
        "fail": "no",
        "subdomains": [
            {"host": "api.coindesk.com"},
            {"host": "api.covidtracking.com"},
            {"host": "api.developer.lifx.com"},
            {"host": "api.fitbit.com"},
            {"host": "api.github.com"},
            {"host": "api.hackaday.io"},
            {"host": "api.hackster.io"},
            {"host": "api.met.no"},
            {"host": "api.nasa.gov"},
            {"host": "api.nytimes.com"},
            {"host": "api.open-meteo.com"},
            {"host": "api.openai.com"},
            {"host": "api.openweathermap.org"},
            {"host": "api.purpleair.com"},
            {"host": "api.spacexdata.com"},
            {"host": "api.thecatapi.com"},
            {"host": "api.thingiverse.com"},
            {"host": "api.thingspeak.com"},
            {"host": "api.tidesandcurrents.noaa.gov"},
            {"host": "api.twitter.com"},
            {"host": "api.wordnik.com"},
        ],
    },
    {
        "heading": "Common hosts",
        "description": "These are other common hosts users hit.",
        "success": "yes",
        "fail": "no",
        "subdomains": [
            {"host": "admiraltyapi.azure-api.net"},
            {"host": "aeroapi.flightaware.com"},
            {"host": "airnowapi.org"},
            {"host": "certification.oshwa.org"},
            {"host": "certificationapi.oshwa.org"},
            {"host": "chat.openai.com"},
            {"host": "covidtracking.com"},
            {"host": "discord.com"},
            {"host": "enviro.epa.gov"},
            {"host": "flightaware.com"},
            {"host": "hosted.weblate.org"},
            {"host": "id.twitch.tv"},
            {"host": "io.adafruit.com"},
            {"host": "jwst.nasa.gov"},
            {"host": "management.azure.com"},
            {"host": "na1.api.riotgames.com"},
            {"host": "oauth2.googleapis.com"},
            {"host": "opensky-network.org"},
            {"host": "opentdb.com"},
            {"host": "raw.githubusercontent.com"},
            {"host": "site.api.espn.com"},
            {"host": "spreadsheets.google.com"},
            {"host": "twitrss.me"},
            {"host": "www.adafruit.com"},
            {"host": "www.alphavantage.co"},
            {"host": "www.googleapis.com"},
            {"host": "www.nhc.noaa.gov"},
            {"host": "www.reddit.com"},
            {"host": "youtube.googleapis.com"},
        ],
    },
    {
        "heading": "Known problem hosts",
        "description": "These are hosts we have run into problems in the past.",
        "success": "yes",
        "fail": "no",
        "subdomains": [
            {"host": "valid-isrgrootx2.letsencrypt.org"},
            {"host": "openaccess-api.clevelandart.org"},
        ],
    },
]

# pulled from:
#  https://github.com/chromium/badssl.com/blob/master/domains/misc/badssl.com/dashboard/sets.js
BADSSL_GROUPS = [
    {
        "heading": "Certificate Validation (High Risk)",
        "description": (
            "If your browser connects to one of these sites, it could be very easy for an attacker "
            "to see and modify everything on web sites that you visit."
        ),
        "success": "no",
        "fail": "yes",
        "subdomains": [
            {"subdomain": "expired"},
            {"subdomain": "wrong.host"},
            {"subdomain": "self-signed"},
            {"subdomain": "untrusted-root"},
        ],
    },
    {
        "heading": "Interception Certificates (High Risk)",
        "description": (
            "If your browser connects to one of these sites, it could be very easy for an attacker "
            "to see and modify everything on web sites that you visit. This may be due to "
            "interception software installed on your device."
        ),
        "success": "no",
        "fail": "yes",
        "subdomains": [
            {"subdomain": "superfish"},
            {"subdomain": "edellroot"},
            {"subdomain": "dsdtestprovider"},
            {"subdomain": "preact-cli"},
            {"subdomain": "webpack-dev-server"},
        ],
    },
    {
        "heading": "Broken Cryptography (Medium Risk)",
        "description": (
            "If your browser connects to one of these sites, an attacker with enough resources may "
            "be able to see and/or modify everything on web sites that you visit. This is because "
            "your browser supports connections settings that are outdated and known to have "
            "significant security flaws."
        ),
        "success": "no",
        "fail": "yes",
        "subdomains": [
            {"subdomain": "rc4"},
            {"subdomain": "rc4-md5"},
            {"subdomain": "dh480"},
            {"subdomain": "dh512"},
            {"subdomain": "dh1024"},
            {"subdomain": "null"},
        ],
    },
    {
        "heading": "Legacy Cryptography (Moderate Risk)",
        "description": (
            "If your browser connects to one of these sites, your web traffic is probably safe "
            "from attackers in the near future. However, your connections to some sites might "
            "not be using the strongest possible security. Your browser may use these settings in "
            "order to connect to some older sites."
        ),
        "success": "maybe",
        "fail": "yes",
        "subdomains": [
            {"subdomain": "tls-v1-0", "port": 1010},
            {"subdomain": "tls-v1-1", "port": 1011},
            {"subdomain": "cbc"},
            {"subdomain": "3des"},
            {"subdomain": "dh2048"},
        ],
    },
    {
        "heading": "Domain Security Policies",
        "description": (
            "These are special tests for some specific browsers. These tests may be able to tell "
            "whether your browser uses advanced domain security policy mechanisms (HSTS, HPKP, SCT"
            ") to detect illegitimate certificates."
        ),
        "success": "maybe",
        "fail": "yes",
        "subdomains": [
            {"subdomain": "revoked"},
            {"subdomain": "pinning-test"},
            {"subdomain": "no-sct"},
        ],
    },
    {
        "heading": "Secure (Uncommon)",
        "description": (
            "These settings are secure. However, they are less common and even if your browser "
            "doesn't support them you probably won't have issues with most sites."
        ),
        "success": "yes",
        "fail": "maybe",
        "subdomains": [
            {"subdomain": "1000-sans"},
            {"subdomain": "10000-sans"},
            {"subdomain": "sha384"},
            {"subdomain": "sha512"},
            {"subdomain": "rsa8192"},
            {"subdomain": "no-subject"},
            {"subdomain": "no-common-name"},
            {"subdomain": "incomplete-chain"},
        ],
    },
    {
        "heading": "Secure (Common)",
        "description": (
            "These settings are secure and commonly used by sites. Your browser will need to "
            "support most of these in order to connect to sites securely."
        ),
        "success": "yes",
        "fail": "no",
        "subdomains": [
            {"subdomain": "tls-v1-2", "port": 1012},
            {"subdomain": "sha256"},
            {"subdomain": "rsa2048"},
            {"subdomain": "ecc256"},
            {"subdomain": "ecc384"},
            {"subdomain": "extended-validation"},
            {"subdomain": "mozilla-modern"},
        ],
    },
]

COMMON_FAILURE_CODES = [
    "Expected 01 but got 00",  # AirLift
    "Failed SSL handshake",  # Espressif
    "MBEDTLS_ERR_SSL_BAD_HS_SERVER_KEY_EXCHANG",  # mbedtls
    "MBEDTLS_ERR_SSL_FATAL_ALERT_MESSAGE",  # mbedtls
    "MBEDTLS_ERR_X509_CERT_VERIFY_FAILED",  # mbedtls
    "MBEDTLS_ERR_X509_FATAL_ERROR",  # mbedtls
]


pool = adafruit_connection_manager.get_radio_socketpool(radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(radio)
connection_manager = adafruit_connection_manager.get_connection_manager(pool)

wifi_ssid = os.getenv("CIRCUITPY_WIFI_SSID")
wifi_password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

if onboard_wifi:
    while not radio.connected:
        radio.connect(wifi_ssid, wifi_password)
else:
    while not radio.is_connected:
        try:
            radio.connect_AP(wifi_ssid, wifi_password)
        except OSError as os_exc:
            print(f"could not connect to AP, retrying: {os_exc}")
            continue


def common_failure(exc):
    text_value = str(exc)
    for common_failures_code in COMMON_FAILURE_CODES:
        if common_failures_code in text_value:
            return True
    return False


def check_group(groups, group_name):
    print(f"\nRunning {group_name}")
    for group in groups:
        print(f'\n - {group["heading"]}')
        success = group["success"]
        fail = group["fail"]
        for subdomain in group["subdomains"]:
            if "host" in subdomain:
                host = subdomain["host"]
            else:
                host = f'{subdomain["subdomain"]}.badssl.com'
            port = subdomain.get("port", 443)
            exc = None
            start_time = time.monotonic()
            try:
                socket = connection_manager.get_socket(
                    host,
                    port,
                    "https:",
                    is_ssl=True,
                    ssl_context=ssl_context,
                    timeout=10,
                )
                connection_manager.close_socket(socket)
            except RuntimeError as e:
                exc = e
            duration = time.monotonic() - start_time

            if fail == "yes" and exc and common_failure(exc):
                result = "passed"
            elif success == "yes" and exc is None:
                result = "passed"
            else:
                result = f"error - success:{success}, fail:{fail}, exc:{exc}"

            print(f"   - {host}:{port} took {duration:.2f} seconds | {result}")


check_group(ADAFRUIT_GROUPS, "Adafruit")
check_group(BADSSL_GROUPS, "BadSSL")
