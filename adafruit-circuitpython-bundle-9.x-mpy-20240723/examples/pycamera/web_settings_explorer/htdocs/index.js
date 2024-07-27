// SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries
//
// SPDX-License-Identifier: MIT
// SPDX-License-Identifier: Unlicense

const html = (strings, ...values) => String.raw({ raw: strings }, ...values);

var ii = 0;

function option_change(k1, k2) {
    var id_ = k1 + "-" + k2;
    var el = document.getElementById(id_)

    url = `/${k1}?k=${k2}&v=${el.value}`
    console.log(url)
    var req = new XMLHttpRequest();
    req.open("GET", url, false)
    req.send();

    document.getElementById("jpeg").src = `/jpeg?${ii++}`
}

function make_controls(k1, t) {
    console.log(t);
    for(var k2 in t) {
        var id_ = k1 + "-" + k2;
        var options = ""
        for(var v in t[k2]) {
            options += html`
            <option value="${v}">${v}</option>
            `
        }
        var ht = html`
        <form >
        <label for="${id_}">${k2}:</label>
        <select id="${id_}" onchange="option_change('${k1}', '${k2}')">
        ${options}
        </select>
        </form>
        `
        console.log(ht);

        var el = document.getElementById("controls")
        el.insertAdjacentHTML("beforeend", ht)
    }
}

for(var k in tunables) {
    console.log(k)
    make_controls(k, tunables[k]);
}
