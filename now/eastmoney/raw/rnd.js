try { (function(d) {
    try {
        var e = d.localStorage
    } catch(b) {}
    function a(g) {
        var i = g.split(".");
        var h = i.length;
        if (i[h - 1] == "com") {
            return (i[h - 2] + "." + i[h - 1])
        } else {
            if (i[h - 1] == "cn") {
                if (i[h - 2] == "com") {
                    return (i[h - 3] + "." + i[h - 2] + "." + i[h - 1])
                } else {
                    return (i[h - 2] + "." + i[h - 1])
                }
            }
        }
        return ""
    }
    var c = a(emtj_currentHostName);
    function f() {
        var g = this;
        this._ec = {};
        this.set = function(h, i) {
            g._evercookie(h,
            function() {},
            i)
        };
        this._evercookie = function(i, h, j) {
            if (g._evercookie === undefined) {
                g = this
            }
            g.evercookie_indexdb_storage(i, j);
            g._ec.cookieData = g.evercookie_cookie(i, j);
            g._ec.localData = g.evercookie_local_storage(i, j)
        };
        this.evercookie_local_storage = function(h, i) {
            try {
                if (e) {
                    e.setItem(h, i)
                }
            } catch(j) {}
        };
        this.evercookie_indexdb_storage = function(j, l) {
            try {
                var i = d.indexedDB || d.mozIndexedDB || d.webkitIndexedDB || d.msIndexedDB;
                if (!i) {
                    return
                }
                var h = 1;
                var k = i.open("idb_evercookie", h);
                k.onerror = function(n) {};
                k.onupgradeneeded = function(p) {
                    var o = p.target.result;
                    var n = o.createObjectStore("evercookie", {
                        keyPath: "name",
                        unique: false
                    })
                };
                k.onsuccess = function(r) {
                    var n = r.target.result;
                    if (n.objectStoreNames.contains("evercookie")) {
                        var p = n.transaction(["evercookie"], "readwrite");
                        var q = p.objectStore("evercookie");
                        var o = q.put({
                            "name": j,
                            "value": l
                        })
                    }
                    n.close()
                }
            } catch(m) {}
        };
        this.evercookie_cookie = function(i, k) {
            var h = new Date();
            var j = 7300;
            h.setTime(h.getTime() + j * 24 * 3600 * 1000);
            document.cookie = i + "=; expires=Mon, 20 Sep 2010 00:00:00 UTC; path=/; domain=" + c;
            document.cookie = i + "=" + encodeURIComponent(k) + ";domain=" + c + ";path=/;expires=" + h.toGMTString()
        }
    }
    d.bigdataEvercookie = f
} (window))
} catch(ex) {} (function(ai) {
var ah = true;
var aG = true;
if (typeof(emtj_logSet) != "undefined" && emtj_logSet.substr(0, 1) == 0) {
    ah = false
}
if (typeof(emtj_logSet) != "undefined" && emtj_logSet.substr(1, 1) == 0) {
    aG = false
}
if (emtj_trueURL.indexOf("isTest=1&") >= 1) {
    setTimeout(function() {
        var aS = h("*[tracker-eventcode]");
        var aV = Array.prototype.slice.call(aS);
        var aR = h("*[data-tracker-eventcode]");
        var aP = Array.prototype.slice.call(aR);
        var aW = aV.concat(aP);
        len = aW.length;
        for (var aQ = 0; aQ < len; ++aQ) {
            var aU = aW[aQ];
            var aT = aU.getAttribute("class");
            var k = aU.getAttribute("tracker-eventcode") || aU.getAttribute("data-tracker-eventcode");
            if (!aT) {
                aT = ""
            }
            aU.setAttribute("class", aT + " " + k)
        }
    },
    3000);
    var ak = true;
    if (emtj_trueURL.indexOf("&openview=false") > 0) {
        ak = false
    }
    var M = J("batchNum");
    var c = J("pageId");
    var V = M + "_" + c + "_pgresult";
    var F = true;
    var aM;
    var Z = {
        result: F,
        mes: aM
    };
    if (typeof(emtj_isUpload) != "undefined" && emtj_isUpload == 0 && ak) {
        aM = "109";
        Z = {
            result: F,
            mes: aM
        };
        localStorage.setItem(V, JSON.stringify(Z));
        return
    }
    if (typeof(emtj_logSet) != "undefined" && !ah && ak) {
        aM = "108";
        Z = {
            result: F,
            mes: aM
        };
        localStorage.setItem(V, JSON.stringify(Z))
    }
}
if (typeof(emtj_isUpload) != "undefined" && emtj_isUpload == 0) {
    return
}
var aA = ai.jQuery || ai.Zepto;
var N = 0;
var a = navigator.userAgent.toLowerCase();
var ab = false;
if (a.indexOf("ttjj") >= 0 || a.indexOf("eastmoney") >= 0) {
    ab = true
}
var ay = "st_";
var C = "20200612";
var aq = "";
var E = "";
var av = "";
var R = "";
var aF = "";
var o = "";
var Q = "";
var aD = "";
var x = "";
var m;
if (typeof(emtj_sampleRate) == "undefined") {
    emtj_sampleRate = 1
}
if (networkProtocol.indexOf("http") >= 0 || networkProtocol.indexOf("https") >= 0) {
    if (emtj_trueURL.indexOf("isTest=1") >= 1) {
        aq = "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_JS_Test.gif";
        E = "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_Event_Test.gif"
    } else {
        aq = "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_JS.gif";
        E = "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_Event.gif";
        fingerUrl = "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_EmToken.gif";
        stayUrl = "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/web_other.gif";
        av = "//bddtlog.eastmoney.com/bd-blink-server/asyncgapi/Web-FirstLoading.gif";
        if (emtj_pageId == 119303304274) {
            R = "//actsl.1234567.com.cn/bd-blink-server/asyncgapi/web_JS0.gif";
            aF = "//actsl.1234567.com.cn/bd-blink-server/asyncgapi/web_Event0.gif";
            o = "//actsl.1234567.com.cn/bd-blink-server/asyncgapi/web_other0.gif"
        } else {
            if (emtj_currentHostName == "xinsanban.eastmoney.com") {
                R = "//xinsanban.eastmoney.com/bd-blink-server/asyncgapi/web_JS.gif";
                aF = "//xinsanban.eastmoney.com/bd-blink-server/asyncgapi/web_Event.gif"
            } else {
                if (emtj_pageId == 119093305971) {
                    R = "//zqhd.eastmoney.com/bd-blink-server/asyncgapi/web_JS_119093305971.gif";
                    aF = "//zqhd.eastmoney.com/bd-blink-server/asyncgapi/web_Event_119093305971.gif";
                    o = "//zqhd.eastmoney.com/bd-blink-server/asyncgapi/web_other_119093305971.gif"
                } else {
                    if (emtj_pageId == 119309306421) {
                        R = "//" + emtj_currentHostName + "/bd-blink-server/asyncgapi/web_JS_119309306421.gif";
                        aF = "//" + emtj_currentHostName + "/bd-blink-server/asyncgapi/web_Event_119309306421.gif";
                        o = "//" + emtj_currentHostName + "/bd-blink-server/asyncgapi/web_other_119309306421.gif"
                    } else {
                        if (emtj_pageId == 119094300302) {
                            R = "//" + emtj_currentHostName + "/bd-blink-server/asyncgapi/web_JS_119094300302.gif";
                            aF = "//" + emtj_currentHostName + "/bd-blink-server/asyncgapi/web_Event_119094300302.gif";
                            o = "//" + emtj_currentHostName + "/bd-blink-server/asyncgapi/web_other_119094300302.gif"
                        }
                    }
                }
            }
        }
    }
} else {
    aq = "https://bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_JS.gif";
    E = "https://bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_Event.gif";
    stayUrl = "https://bdwblog.eastmoney.com/bd-blink-server/asyncgapi/web_other.gif";
    av = "https://bddtlog.eastmoney.com/bd-blink-server/asyncgapi/Web-FirstLoading.gif"
}
var Y = "";
var aw = "";
var n = emtj_getUI();
var af = "";
var aE = "";
var O = "";
var aJ = "4.5.2";
var s = false;
var aB = "";
var B = "";
var aj = "";
var b = "";
var S = "";
var e = "";
var D = "";
var ax = "";
var j = "";
var aa = "";
var G = "";
var r = "";
var ag = "";
var z = aL();
var aK = -1;
var X = new bigdataEvercookie();
var w = new bigdataEvercookie();
var am = new bigdataEvercookie();
try {
    var au = window.localStorage
} catch(aN) {}
var I = emtj_getCookie("qgqp_b_id");
var ac = undefined;
var K = !!(window.attachEvent && !window.opera);
var y = document.getElementsByTagName("script");
if (y.length > 0) {
    for (var L = 0; L < y.length; L++) {
        var g = y[L].src;
        if (g && g.indexOf("jump_tracker.js") >= 0 && g.indexOf("stg") >= 0) {
            if (networkProtocol.indexOf("http") >= 0 || networkProtocol.indexOf("https") >= 0) {
                if (emtj_trueURL.indexOf("isTest=1") >= 1) {
                    aq = "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_JS_Test.gif";
                    E = "//bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_Event_Test.gif"
                } else {
                    aq = "//blinkhd.eastmoney.com/bd-blink-server/asyncgapi/T_Web_JS.gif";
                    E = "//blinkhd.eastmoney.com/bd-blink-server/asyncgapi/T_Web_Event.gif";
                    fingerUrl = "//stg-bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_EmToken.gif";
                    stayUrl = "//stg-bdwblog.eastmoney.com/bd-blink-server/asyncgapi/web_other.gif";
                    av = "//stg-bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web-FirstLoading.gif";
                    if (emtj_pageId == 119303304274) {
                        R = "//actsl.1234567.com.cn/bd-blink-server/asyncgapi/web_JS0.gif";
                        aF = "//actsl.1234567.com.cn/bd-blink-server/asyncgapi/web_Event0.gif";
                        o = "//actsl.1234567.com.cn/bd-blink-server/asyncgapi/web_other0.gif"
                    }
                }
            } else {
                aq = "https://stg-bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_JS.gif";
                E = "https://stg-bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web_Event.gif";
                stayUrl = "https://stg-bdwblog.eastmoney.com/bd-blink-server/asyncgapi/web_other.gif";
                av = "https://stg-bdwblog.eastmoney.com/bd-blink-server/asyncgapi/Web-FirstLoading.gif"
            }
        }
    }
}
v(ay + "orirUrl");
function ap() {
    af = l();
    aE = emtj_getCookie(ay + "si");
    if (!aE) {
        aE = emtj_getRandomStrBy(14);
        aI(ay + "si", aE)
    }
    if (aK == 0 || aK == 5 || aK == 2) {
        return
    }
    emtj_pviUVNO = emtj_getCookie(ay + "pvi");
    if (emtj_pviUVNO) {
        aK = 1
    }
    O = emtj_getCookie(ay + "sp");
    orirUrl = emtj_getCookie(ay + "inirUrl");
    if (!emtj_pviUVNO) {
        if (au && au.getItem("st_pvi")) {
            emtj_pviUVNO = au.getItem("st_pvi");
            O = au.getItem("st_sp");
            orirUrl = au.getItem("st_inirUrl");
            aK = 2
        } else {
            if (z) {
                at("st_pvi");
                at("st_sp");
                at("st_inirUrl")
            }
        }
    }
    if (emtj_pviUVNO) {
        X.set("st_pvi", emtj_pviUVNO);
        if (!O) {
            O = emtj_getNowFormatDate(new Date(), 2)
        }
        w.set("st_sp", O);
        if (!orirUrl) {
            orirUrl = document.referrer.split("?")[0]
        }
        am.set("st_inirUrl", orirUrl)
    } else {
        if (z) {
            setTimeout(function() {
                if (emtj_pviUVNO) {
                    X.set("st_pvi", emtj_pviUVNO);
                    if (!O) {
                        O = emtj_getNowFormatDate(new Date(), 2)
                    }
                    w.set("st_sp", O);
                    if (!orirUrl) {
                        orirUrl = document.referrer.split("?")[0]
                    }
                    am.set("st_inirUrl", orirUrl)
                } else {
                    al()
                }
            },
            50)
        } else {
            al()
        }
    }
}
ap();
function al() {
    emtj_pviUVNO = emtj_getRandomStrBy(14);
    X.set("st_pvi", emtj_pviUVNO);
    O = emtj_getNowFormatDate(new Date(), 2);
    w.set("st_sp", O);
    orirUrl = document.referrer.split("?")[0];
    am.set("st_inirUrl", orirUrl);
    aK = 0
}
function aL() {
    if (window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB) {
        return true
    } else {
        return false
    }
}
function at(k) {
    try {
        var i = 1;
        var aP = indexedDB.open("idb_evercookie", i);
        aP.onerror = function(aR) {};
        aP.onupgradeneeded = function(aT) {
            var aS = aT.target.result;
            var aR = aS.createObjectStore("evercookie", {
                keyPath: "name",
                unique: false
            })
        };
        aP.onsuccess = function(aV) {
            var aR = aV.target.result;
            if (!aR.objectStoreNames.contains("evercookie")) {
                self._ec.idbData = undefined
            } else {
                var aT = aR.transaction(["evercookie"]);
                var aU = aT.objectStore("evercookie");
                var aS = aU.get(k);
                aS.onsuccess = function(aW) {
                    if (emtj_pviUVNO && (aK == 0 || aK == 1)) {
                        return
                    }
                    if (aS.result) {
                        if (k == "st_pvi") {
                            emtj_pviUVNO = aS.result.value;
                            aK = 5
                        } else {
                            if (k == "st_sp") {
                                O = aS.result.value
                            } else {
                                if (k == "st_inirUrl") {
                                    orirUrl = aS.result.value
                                }
                            }
                        }
                    }
                }
            }
            aR.close()
        }
    } catch(aQ) {}
}
function A() {
    var k = document.location.toString();
    var i = k.split("?");
    if (i.length > 1) {
        x = "?" + i[1];
        return x
    }
    return ""
}
function l() {
    if (networkProtocol.indexOf("http") < 0 && networkProtocol.indexOf("https") < 0) {
        return an()
    } else {
        return window.location.href.replace(/(^\s*)|(\s*$)/g, "")
    }
}
function an() {
    x = A();
    if (y.length > 0) {
        for (var i = 0; i < y.length; i++) {
            var aP = y[i].src;
            if (aP && aP.indexOf("jump_tracker.js") >= 0 || aP && aP.indexOf("emtj_tracker.js") >= 0) {
                Q = y[i].getAttribute("emtj-url");
                aD = y[i].getAttribute("emtj-param")
            }
        }
    }
    if (aD == null) {
        aD = ""
    }
    if (aD != "" && x != "") {
        aD = "&" + aD + "&isFile=1"
    } else {
        if (aD != "" && x == "") {
            aD = "?" + aD + "&isFile=1"
        } else {
            if (aD == "" && x == "") {
                aD = "?isFile=1"
            } else {
                if (aD == "" && x != "") {
                    aD = "&isFile=1"
                }
            }
        }
    }
    return (Q + x + aD).replace(/(^\s*)|(\s*$)/g, "")
}
function H(aQ, aP) {
    var i = aQ.split(".");
    var k = aP.split(".");
    if (i[0] * 1 > k[0] * 1) {
        return true
    }
    if (i[0] * 1 >= k[0] * 1 && i[1] * 1 > k[1] * 1) {
        return true
    }
    if (i[0] * 1 >= k[0] * 1 && i[1] * 1 >= k[1] * 1 && i[2] * 1 > k[2] * 1) {
        return true
    }
    return false
}
function d() {
    var i = navigator.userAgent.toLowerCase();
    if (i.indexOf("iphone") >= 0) {
        return "iphone"
    }
    if (i.indexOf("android") >= 0) {
        return "android"
    }
    if (i.indexOf("ipad") >= 0) {
        return "ipad"
    }
    return ""
}
function ad(i) {
    var aP = i.split(".");
    var k = aP.length;
    if (aP[k - 1] == "com") {
        return (aP[k - 2] + "." + aP[k - 1])
    } else {
        if (aP[k - 1] == "cn") {
            if (aP[k - 2] == "com") {
                return (aP[k - 3] + "." + aP[k - 2] + "." + aP[k - 1])
            } else {
                return (aP[k - 2] + "." + aP[k - 1])
            }
        }
    }
    return ""
}
function aI(i, aQ, aR) {
    var aP = ad(emtj_currentHostName);
    if (!aR) {
        document.cookie = i + "=" + encodeURIComponent(aQ) + ";domain=" + aP + ";path=/";
        return
    }
    var k = W(aR);
    var aS = new Date();
    aS.setTime(aS.getTime() + k * 1);
    document.cookie = i + "=" + encodeURIComponent(aQ) + ";domain=" + aP + ";path=/;expires=" + aS.toGMTString()
}
function W(aP) {
    var k = aP.substring(1, aP.length) * 1;
    var i = aP.substring(0, 1);
    if (i == "s") {
        return k * 1000
    } else {
        if (i == "h") {
            return k * 60 * 60 * 1000
        } else {
            if (i == "d") {
                return k * 24 * 60 * 60 * 1000
            }
        }
    }
}
function v(i) {
    var k = ad(emtj_currentHostName);
    var aQ = new Date();
    aQ.setTime(aQ.getTime() - 1);
    var aP = emtj_getCookie(i);
    if (aP != null) {
        document.cookie = i + "=" + aP + ";domain=" + k + ";path=/;expires=" + aQ.toGMTString()
    }
}
function u(aP, aR, k, i) {
    if (i) {
        var aQ = k;
        k = function(aS) {
            aQ.call(aP, aS)
        }
    }
    if (aP.addEventListener) {
        aP.addEventListener(aR, k)
    } else {
        if (aP.attachEvent) {
            aP.attachEvent("on" + aR, k)
        } else {
            aP["on" + aR] = k
        }
    }
    return k
}
function q(k, aP, i) {
    if (k.removeEventListener) {
        k.removeEventListener(aP, i)
    } else {
        if (k.detachEvent) {
            k.detachEvent("on" + aP, i)
        } else {
            k["on" + aP] = null
        }
    }
}
function h(a1) {
    if (aA) {
        return aA(a1)
    }
    var a2 = /([\*a-zA-Z1-6]*)?(\[(\w+)\s*(\^|\$|\*|\||~|!)?=?\s*([\w\u00C0-\uFFFF\s\-_\.]+)?\])?/,
    aS = arguments[1] || document,
    aU = a1.match(a2),
    a2 = aU[1] || "*",
    aQ = aU[3],
    aX = aU[4] + "=",
    aY = aU[5],
    aZ = {
        "class": "className",
        "for": "htmlFor"
    },
    aT = [],
    k = (a2 === "*" && aS.all) ? aS.all: aS.getElementsByTagName(a2),
    aP = k.length;
    if (( !! document.querySelectorAll) && aX != "!=") {
        k = document.querySelectorAll(a1);
        for (var aV = 0,
        aP = k.length; aV < aP; aV++) {
            aT.push(k[aV])
        }
        return aT
    }
    if (!+"\v1") {
        aQ = aZ[aQ] ? aZ[aQ] : aQ
    }
    while (aP--) {
        var aW = k[aP],
        a0 = !+"\v1" ? aW[aQ] : aW.getAttribute(aQ);
        if (typeof a0 === "string" && a0.length > 0) {
            if ( !! aY) {
                var aR = aX === "=" ? a0 === aY: aX === "!=" ? a0 != aY: aX === "*=" ? a0.indexOf(aY) >= 0 : aX === "~=" ? (" " + a0 + " ").indexOf(aY) >= 0 : aX === "^=" ? a0.indexOf(aY) === 0 : aX === "$=" ? a0.slice( - aY.length) === aY: aX === "|=" ? a0 === aY || a0.substring(0, aY.length + 1) === aY + "-": false;
                aR && aT.push(aW)
            } else {
                aT.push(aW)
            }
        }
    }
    return aT
}
function ar(aQ) {
    var aP = [];
    for (var i in aQ) {
        aP.push(i + "=" + encodeURIComponent(aQ[i]))
    }
    var aR = aP.join("&");
    P(aq + "?" + aR);
    if (emtj_pageId == 119303304274 || emtj_currentHostName == "xinsanban.eastmoney.com" || emtj_pageId == 119093305971 || emtj_pageId == 119309306421 || emtj_pageId == 119094300302) {
        P(R + "?" + aR)
    }
}
function J(aP) {
    var k = [];
    var aT = "";
    var aU = window.location.href.split("?")[1];
    k = aU.split("&");
    for (var aQ = 0; aQ < k.length; aQ++) {
        if (k[aQ].indexOf("#") == -1) {
            aT += "&" + k[aQ]
        }
    }
    var aR = new RegExp("(^|&)" + aP + "=([^&]*)(&|$)");
    var aS = aT.match(aR);
    if (aS != null) {
        return decodeURIComponent(aS[2])
    }
    return null
}
function P(k) {
    if (emtj_trueURL.indexOf("isTest=1&") >= 1) {
        var aS = M + "_" + c + "_data";
        var aQ = localStorage.getItem(aS);
        var aP = k + "&jsVersion=" + C;
        if (!aQ) {
            localStorage.setItem(aS, aP)
        } else {
            localStorage.setItem(aS, aQ + "@@@@@" + aP)
        }
    }
    function aT(aU) {
        if (emtj_trueURL.indexOf("isTest=1&") >= 1) {
            if (k.indexOf("Web_JS") > 0) {
                V = M + "_" + c + "_pgresult";
                if (typeof(emtj_isUpload) == "undefined") {
                    aU = false;
                    aM = 101
                } else {
                    if (c != emtj_pageId) {
                        aU = false;
                        aM = 104
                    } else {
                        if (aU == false) {
                            aM = 102
                        }
                    }
                }
            } else {
                if (k.indexOf("Web_Event") > 0) {
                    V = M + "_" + c + "_ecresult";
                    if (aU == false) {
                        aM = 102
                    }
                }
            }
            if (aU == true) {
                aM = 200
            }
            Z = {
                result: aU,
                mes: aM
            };
            localStorage.setItem(V, JSON.stringify(Z))
        }
    }
    var i = new Image();
    var aR = "_img_" + Math.random();
    window[aR] = i;
    i.onload = function() {
        window[aR] = null;
        aT(true)
    };
    i.onerror = function(aU) {
        window[aR] = null;
        aT(false)
    };
    i.src = k + "&jsVersion=" + C
}
function U(aR, aP, aQ, i, k) {
    N++;
    m = emtj_userActionId + "-" + aQ + "-" + N;
    af = l();
    aI(ay + "asi", m);
    P(E + "?elem=" + aR + "&EventType=" + aP + "&EventCode=" + encodeURIComponent(aQ) + "&ExtInfo=" + encodeURIComponent(i) + "&UID=" + n + "&UVNO=" + emtj_pviUVNO + "&url=" + encodeURIComponent(af) + "&gtu=" + encodeURIComponent(k) + "&deviceId=" + B + "&deviceType=" + aj + "&tradeID=" + b + "&tradeIDType=" + S + "&phoneModle=" + e + "&preEventCode=" + D + "&gt=" + ax + "&appKey=" + aa + "&deviceBrand=" + G + "&phoneAppVersion=" + j + "&appSeid=" + r + "&appEuid=" + ag + "&sr=" + emtj_sampleRate + "&pi=" + emtj_pageId + "&mt=" + encodeURIComponent(m) + "&passc=" + I + "&cerr=" + aw);
    if (emtj_pageId == 119303304274 || emtj_currentHostName == "xinsanban.eastmoney.com" || emtj_pageId == 119093305971 || emtj_pageId == 119309306421 || emtj_pageId == 119094300302) {
        P(aF + "?elem=" + aR + "&EventType=" + aP + "&EventCode=" + encodeURIComponent(aQ) + "&ExtInfo=" + encodeURIComponent(i) + "&UID=" + n + "&UVNO=" + emtj_pviUVNO + "&url=" + encodeURIComponent(af) + "&gtu=" + encodeURIComponent(k) + "&deviceId=" + B + "&deviceType=" + aj + "&tradeID=" + b + "&tradeIDType=" + S + "&phoneModle=" + e + "&preEventCode=" + D + "&gt=" + ax + "&appKey=" + aa + "&deviceBrand=" + G + "&phoneAppVersion=" + j + "&appSeid=" + r + "&appEuid=" + ag + "&sr=" + emtj_sampleRate + "&pi=" + emtj_pageId + "&mt=" + encodeURIComponent(m) + "&passc=" + I + "&cerr=" + aw)
    }
}
function t(k) {
    var aP = [];
    for (var aQ = 0; aQ < k.length; aQ++) {
        if (aP.indexOf(k[aQ]) == -1) {
            aP.push(k[aQ])
        }
    }
    return aP
}
function az(i) {
    return i.split("").reverse().join("")
}
function aH(i, k) {
    if (!k) {
        k = ""
    }
    if (emtj_pviUVNO || !z) {
        P(av + "?url=" + encodeURIComponent(af) + "&pi=" + emtj_pageId + "&pvi=" + emtj_pviUVNO + "&mt=" + emtj_userActionId + "&ui=" + n + "&ua=" + a + "&firstime=" + i + "&deinfo=" + k)
    } else {
        if (z) {
            setTimeout(function() {
                P(av + "?url=" + encodeURIComponent(af) + "&pi=" + emtj_pageId + "&pvi=" + emtj_pviUVNO + "&mt=" + emtj_userActionId + "&ui=" + n + "&ua=" + a + "&firstime=" + i + "&deinfo=" + k)
            },
            50)
        }
    }
}
var ae = function() {
    if (ab) {
        k()
    } else {
        i()
    }
    function i() {
        var aQ = new Date();
        var aR = {};
        aR.url = af;
        aR.rUrl = document.referrer.replace(/<\/?.+?>/g, "").replace(/[\r\n]/g, "");
        aR.si = aE;
        aR.sn = parseInt(emtj_getCookie(ay + "sn")) + 1;
        if (!aR.sn) {
            aR.sn = 1
        }
        aI(ay + "sn", aR.sn);
        aR.scr = window.screen.width + "x" + window.screen.height;
        aR.dpr = window.devicePixelRatio;
        var aW = "";
        if (navigator.language) {
            aW = navigator.language
        } else {
            aW = navigator.browserLanguage
        }
        aR.lg = aW;
        aR.tz = "" + (aQ.getTimezoneOffset() / 60 * -1);
        if (typeof(emtj_startTime) != "undefined") {
            var aP = emtj_startTime
        } else {
            aP = 0
        }
        aR.domreadyt = emtj_endTime - aP;
        aR.wt = -1;
        if (window.performance || window.webkitPerformance || window.msPerformance || window.mozPerformance) {
            var aV = window.performance || window.webkitPerformance || window.msPerformance || window.mozPerformance;
            aR.domreadyt = aV.timing.domContentLoadedEventEnd - aV.timing.navigationStart;
            aR.wt = aV.timing.responseStart - aV.timing.navigationStart
        }
        var aS = emtj_getCookie(ay + "psi");
        var aU = emtj_getCookie(ay + "asi");
        if (!aS) {
            aR.psi = ""
        } else {
            aR.psi = aS
        }
        if (!aU) {
            aR.asi = ""
        } else {
            aR.asi = aU
        }
        aI(ay + "psi", emtj_userActionId);
        aI(ay + "asi", "delete");
        aR.ui = n;
        aR.deviceId = "";
        aR.deviceType = "";
        var aT = emtj_getCookie("fund_trade_trackid");
        if (!aT || aT == "undefined" || aT == undefined) {
            aR.tradeID = "";
            aR.tradeIDType = ""
        } else {
            aR.tradeID = aT;
            aR.tradeIDType = 2
        }
        aR.phoneModle = "";
        aR.preEventCode = "";
        aR.gt = "";
        aR.phoneAppVersion = "";
        aR.appKey = "";
        aR.deviceBrand = "";
        aR.appSeid = "";
        aR.appEuid = "";
        if (s == true) {
            return
        } else {
            if (aB != "") {
                n = aR.ui = emtj_appUID;
                aR.deviceId = B;
                aR.deviceType = aj;
                aR.tradeID = b;
                aR.tradeIDType = S;
                aR.phoneModle = e;
                aR.preEventCode = D;
                aR.gt = ax;
                aR.phoneAppVersion = j;
                aR.appKey = aa;
                aR.deviceBrand = G;
                aR.appSeid = r;
                aR.appEuid = ag
            }
        }
        aR.pi = emtj_pageId;
        aR.mt = emtj_userActionId;
        aR.err = Y;
        aR.tus = "";
        aR.eti = "";
        aR.passc = I;
        if (emtj_pviUVNO || !z) {
            aR.pvi = emtj_pviUVNO;
            aR.sp = O;
            aR.orirUrl = orirUrl;
            aR.extinfo = aK;
            ar(aR);
            aK = 1
        } else {
            if (z) {
                setTimeout(function() {
                    aR.pvi = emtj_pviUVNO;
                    aR.sp = O;
                    aR.orirUrl = orirUrl;
                    aR.extinfo = aK;
                    ar(aR);
                    aK = 1
                },
                50)
            }
        }
    }
    function k() {
        function aS(aV) {
            var aV = aV;
            var aW = document.createElement("iframe");
            aW.style.width = "1px";
            aW.style.height = "1px";
            aW.style.display = "none";
            aW.src = aV;
            document.body.appendChild(aW);
            setTimeout(function() {
                aW.remove()
            },
            1000)
        }
        if (a.indexOf("ttjj") >= 0) {
            var aQ = a.match(/ttjj\/(.*)[\s]*/);
            if (aQ != null) {
                j = aQ = aQ[1];
                window.logsession = function(aV) {
                    aB = JSON.stringify(aV);
                    try {
                        if (!aV.DeviceId) {
                            B = ""
                        } else {
                            B = window.btoa(az(emtj_getRandomStrBy(6) + "-" + aV.DeviceId))
                        }
                        emtj_appUID = aV.UID;
                        aj = aV.DeviceType;
                        b = aV.TradeID;
                        if (b != "") {
                            S = 2
                        } else {
                            S = ""
                        }
                        D = aV.preEventCode;
                        if (!aV.preEventCode) {
                            D = ""
                        }
                        if (!aV.phoneModle) {
                            e = ""
                        } else {
                            e = aV.phoneModle
                        }
                        if (!aV.deviceBrand) {
                            G = ""
                        } else {
                            G = aV.deviceBrand
                        }
                        if (!aV.appKey) {
                            aa = ""
                        } else {
                            aa = aV.appKey
                        }
                        if (!aV.euid) {
                            ag = ""
                        } else {
                            ag = window.btoa(az(emtj_getRandomStrBy(6) + "-" + aV.euid))
                        }
                    } catch(aW) {
                        Y = aW
                    }
                    s = false;
                    i()
                };
                if (H(aQ, aJ)) {
                    s = true;
                    aS('emfundapp:applogsession({"callbackMethodName":"logsession"})')
                } else {
                    s = false;
                    i()
                }
            }
        } else {
            if (a.indexOf("eastmoney") >= 0 && !(a.indexOf("hap") >= 0 && a.indexOf("com.eastmoney.marketingapp") >= 0)) {
                var aT = true;
                s = true;
                setonReady = setTimeout(function() {
                    aT = false;
                    s = false;
                    i()
                },
                1000);
                window.cb_appinfo = function(aV) {
                    aB = aV;
                    var aX = JSON.parse(aV.replace(/\n/g, "\\\\n").replace(/\r/g, "\\\\r"));
                    try {
                        if (!aX.data.deviceInfo.deviceID) {
                            B = ""
                        } else {
                            B = window.btoa(az(emtj_getRandomStrBy(6) + "-" + aX.data.deviceInfo.deviceID))
                        }
                        if (!aX.data.passport || !aX.data.passport.uid) {
                            emtj_appUID = ""
                        } else {
                            emtj_appUID = aX.data.passport.uid
                        }
                        aj = aX.data.deviceInfo.deviceType;
                        if (!aX.data.trade || !aX.data.trade.length || !aX.data.trade[0].tradeCustomId) {
                            b = "";
                            S = ""
                        } else {
                            b = aX.data.trade[0].tradeCustomId;
                            S = 1
                        }
                        e = aX.data.deviceInfo.phoneModle;
                        if (!aX.data.deviceInfo.gToken) {
                            ax = ""
                        } else {
                            ax = aX.data.deviceInfo.gToken
                        }
                        j = aX.data.deviceInfo.appversion;
                        if (!aX.data.deviceInfo.appKey && aX.data.deviceInfo.ProductType == "uufund") {
                            aa = "62yhha34"
                        } else {
                            if (!aX.data.deviceInfo.appKey) {
                                aa = ""
                            } else {
                                aa = aX.data.deviceInfo.appKey
                            }
                        }
                        if (!aX.data.deviceInfo.deviceBrand) {
                            G = ""
                        } else {
                            G = aX.data.deviceInfo.deviceBrand
                        }
                        D = "";
                        if (!aX.data.deviceInfo.appSessionid) {
                            r = ""
                        } else {
                            r = aX.data.deviceInfo.appSessionid
                        }
                        if (!aX.data.deviceInfo.euid) {
                            ag = ""
                        } else {
                            ag = window.btoa(az(emtj_getRandomStrBy(6) + "-" + aX.data.deviceInfo.euid))
                        }
                    } catch(aW) {
                        Y = aW
                    }
                    if (aT) {
                        clearTimeout(setonReady);
                        s = false;
                        i()
                    }
                };
                var aU = '{"callbackname": "cb_appinfo","type": "passport,deviceInfo,trade"}';
                function aP() {
                    if (/(iPhone|iPod|iPad|iTouch|iOS)/i.test(navigator.userAgent)) {
                        return true
                    } else {
                        return false
                    }
                }
                function aR() {
                    if (aP()) {
                        if (emtj_currentHostName == "gubatestapi.eastmoney.com" || emtj_currentHostName == "gubaapi.eastmoney.com" || emtj_currentHostName == "gubaapihttps.eastmoney.com") {
                            if (a.indexOf("appversion_") >= 0) {
                                aS("h5GetModuleInfo:" + aU)
                            } else {
                                clearTimeout(setonReady);
                                aT = false;
                                s = false;
                                i()
                            }
                        } else {
                            aS("h5GetModuleInfo:" + aU)
                        }
                    } else {
                        prompt("h5GetModuleInfo", aU + "$&&$java.lang.String")
                    }
                }
                aR()
            }
        }
    }
};
var T = function() {
    function i() {
        var aQ = d();
        if (aQ) {
            var aP = {
                tap: function(aT, aU) {
                    var aS, aR, aV = 10;
                    aT.addEventListener("touchstart",
                    function(aX) {
                        var aW = aX.targetTouches[0];
                        aS = aW.pageX;
                        aR = aW.pageY
                    },
                    false);
                    aT.addEventListener("touchend",
                    function(aY) {
                        var aX = aY.changedTouches[0],
                        aW = aX.pageX,
                        aZ = aX.pageY;
                        if (Math.abs(aS - aW) < aV && Math.abs(aR - aZ) < aV) {
                            aU()
                        }
                    },
                    false)
                }
            };
            aP.tap(document, k)
        } else {
            u(document.body, "mousedown", k, true)
        }
    }
    function k(aU) {
        var aV = emtj_willHandle(emtj_sampleRate);
        if (!aV) {
            return
        }
        aU = aU || window.event;
        var aX = aU.target || aU.srcElement;
        var aQ = aX.tagName;
        var aT = 0;
        var aW = aX.getAttribute("href");
        try {
            while (!aX.getAttribute("tracker-eventcode") && !aX.getAttribute("data-tracker-eventcode") && aT < 5) {
                if (aX == document.body || aX == document.documentElement) {
                    return
                }
                aT++;
                aX = aX.parentNode
            }
            var aS = aX.getAttribute("tracker-eventcode") || aX.getAttribute("data-tracker-eventcode");
            if (aS) {
                var aP = aX.getAttribute("tracker-extinfo") || aX.getAttribute("data-tracker-extinfo");
                if (!aW) {
                    aW = ""
                }
                U(aQ, "click", aS, aP, aW)
            }
        } catch(aR) {
            aw = aR
        }
    }
    i()
};
var aO = function() {
    var be = -1;
    var bg = -1;
    var bb = -1;
    var aV = [];
    var ba = 0;
    var aP = mainPage = 0;
    var aZ = 0;
    var bc = 0;
    var a8, a3;
    var a4 = 0;
    var a2;
    var bd = "in";
    var bo = false;
    var a9 = 10;
    var a5 = "default";
    var bl = 0;
    var a7 = l();
    if (window.performance || window.webkitPerformance || window.msPerformance || window.mozPerformance) {
        var a6 = window.performance || window.webkitPerformance || window.msPerformance || window.mozPerformance;
        var bj = a6.timing;
        emtj_startTime = bj.navigationStart;
        a8 = new Date(emtj_startTime);
        a3 = emtj_getNowFormatDate(a8, 2);
        bi(emtj_startTime)
    } else {
        if (typeof(emtj_startTime) != "undefined") {
            a8 = new Date(emtj_startTime);
            a3 = emtj_getNowFormatDate(a8, 2);
            bi(emtj_startTime)
        }
    }
    function bn() {
        if (bd == "in") {
            a9 = 10
        }
    }
    function bi(br) {
        bl = document.documentElement.scrollTop || document.body.scrollTop || window.pageYOffset;
        aV.push(bl);
        window.keeptime = setInterval(function() {
            a9 -= 1;
            if (0 == a9) {
                bd = "out";
                bo = true;
                a5 = "wait";
                aR();
                clearInterval(keeptime)
            }
        },
        1000);
        var i = {
            tap: function(bv, bw) {
                var bu, bt, bx = 10;
                bv.addEventListener("touchstart",
                function(bz) {
                    var by = bz.targetTouches[0];
                    bu = by.pageX;
                    bt = by.pageY
                },
                false);
                bv.addEventListener("touchend",
                function(bA) {
                    var bz = bA.changedTouches[0],
                    by = bz.pageX,
                    bB = bz.pageY;
                    if (Math.abs(bu - by) < bx && Math.abs(bt - bB) < bx) {
                        bw()
                    } else {
                        if (Math.abs(bu - by) > bx || Math.abs(bt - bB) > bx) {
                            bw()
                        }
                    }
                },
                false)
            }
        };
        i.tap(document, bn);
        function bs(bu) {
            var bv = document.getElementsByTagName(bu);
            for (var bt = 0; bt < bv.length; bt++) {
                if (bv[bt].type == "text" || bv[bt].type == "textarea" || bv[bt].type == "select-one") {
                    bv[bt].addEventListener("input",
                    function() {
                        bn()
                    },
                    false)
                }
            }
        }
        bs("input");
        bs("textarea");
        bs("select")
    }
    function aU() {
        var bu = document.querySelector(".info-info");
        var br = bu.innerText.length;
        var bt = br / 400 * 60;
        var bs = 0;
        var bv = bu.getElementsByTagName("img");
        if (bv.length) {
            var bw = 6;
            for (var i = 0; i < bv.length; i++) {
                if (i >= 2) {
                    bw = 3
                } else {
                    bw = bw - 1
                }
                bs = bs + bw
            }
        }
        bc = Math.round(bt + bs)
    }
    function aR() {
        a2 = new Date();
        var br = emtj_getNowFormatDate(a2, 2);
        a4 = (a2.getTime() - emtj_startTime) / 1000;
        aZ = window.innerHeight || document.documentElement.clientHeight;
        aP = document.documentElement.scrollHeight;
        if (aZ) {
            be = Math.floor(aP / aZ * 100) / 100
        }
        if (document.querySelector(".info-info") && aZ) {
            mainPage = document.querySelector(".info-info").offsetHeight + document.querySelector(".info-info").offsetTop;
            bg = Math.floor(mainPage / aZ * 100) / 100;
            aU()
        }
        var i = t(aV);
        if (i.length > 1 && aZ) {
            ba = Math.max.apply(null, i);
            bb = Math.floor((ba / aZ + 1) * 100) / 100
        } else {
            if (aZ) {
                bl = document.documentElement.scrollTop || document.body.scrollTop || window.pageYOffset;
                bb = Math.floor((bl / aZ + 1) * 100) / 100
            }
        }
        P(stayUrl + "?url=" + encodeURIComponent(a7) + "&st=" + a4 + "&sd=" + a3 + "&ed=" + br + "&mt=" + emtj_userActionId + "&pvi=" + emtj_pviUVNO + "&si=" + aE + "&flag=" + bo + "&type=" + "stayTime" + "&snum=" + be + "&msc=" + bg + "&maxsc=" + bb + "&estime=" + bc + "&leavet=" + a5 + "&rnd=" + Math.random());
        if (emtj_pageId == 119303304274 || emtj_pageId == 119093305971 || emtj_pageId == 119309306421 || emtj_pageId == 119094300302) {
            P(o + "?url=" + encodeURIComponent(a7) + "&st=" + a4 + "&sd=" + a3 + "&ed=" + br + "&mt=" + emtj_userActionId + "&pvi=" + emtj_pviUVNO + "&si=" + aE + "&flag=" + bo + "&type=" + "stayTime" + "&snum=" + be + "&msc=" + bg + "&maxsc=" + bb + "&estime=" + bc + "&leavet=" + a5 + "&rnd=" + Math.random())
        }
    }
    window.addEventListener("scroll", bk, false);
    if (!Date.now) {
        Date.now = function() {
            return new Date().getTime()
        }
    }
    var aS = ["webkit", "moz"];
    for (var bm = 0; bm < aS.length && !window.requestAnimationFrame; ++bm) {
        var a0 = aS[bm];
        window.requestAnimationFrame = window[a0 + "RequestAnimationFrame"]
    }
    if (/iP(ad|hone|od).*OS 6/.test(window.navigator.userAgent) || !window.requestAnimationFrame) {
        var bq = 0;
        window.requestAnimationFrame = function(bs) {
            var br = Date.now();
            var i = Math.max(bq + 16, br);
            return setTimeout(function() {
                bs(bq = i)
            },
            i - br)
        }
    }
    scheduledAnimationFrame = false;
    function bk() {
        if (scheduledAnimationFrame) {
            return
        }
        scheduledAnimationFrame = true;
        window.requestAnimationFrame(function() {
            scheduledAnimationFrame = false;
            bn();
            bl = document.documentElement.scrollTop || document.body.scrollTop || window.pageYOffset;
            aV.push(bl)
        })
    }
    function aQ() {
        if (bd == "in") {
            bd = "out";
            clearInterval(keeptime);
            aR()
        }
    }
    if (a.indexOf("iphone") >= 0 || a.indexOf("ipad") >= 0 || a.indexOf("android") >= 0) {
        window.addEventListener("pagehide", bf, false)
    } else {
        window.addEventListener("beforeunload", k, false)
    }
    function bf() {
        a5 = "pagehide";
        aQ()
    }
    function k() {
        a5 = "beforeunload";
        aQ()
    }
    var a1 = !!(window.history && history.pushState);
    if (a1) {
        var bp = function(i) {
            var br = window.history[i];
            return function() {
                var bt = br.apply(this, arguments);
                var bs = new Event(i.toLowerCase());
                bs.arguments = arguments;
                window.dispatchEvent(bs);
                return bt
            }
        };
        window.history.pushState = bp("pushState");
        window.history.replaceState = bp("replaceState")
    }
    window.addEventListener("pushstate", aT, false);
    window.addEventListener("replacestate", aT, false);
    window.addEventListener("popstate", aT, false);
    function aT(i) {
        a5 = "spa";
        aQ();
        emtj_startTime = new Date().getTime();
        a8 = new Date(emtj_startTime);
        a3 = emtj_getNowFormatDate(a8, 2);
        a4 = 0;
        bo = false;
        a9 = 10;
        bd = "in";
        a5 = "default";
        aV = [];
        bg = -1;
        bc = 0;
        a7 = l();
        bi(emtj_startTime)
    }
    function aY() {
        var bs = ["webkit", "moz", "ms", "o"];
        if ("hidden" in document) {
            return "hidden"
        }
        for (var br = 0; br < bs.length; br++) {
            if ((bs[br] + "Hidden") in document) {
                return bs[br] + "Hidden"
            }
        }
        return null
    }
    var aX = aY();
    if (aX) {
        var bh = aX.replace(/[H|h]idden/, "") + "visibilitychange";
        document.addEventListener(bh, aW, false)
    }
    function aW() {
        if (document[aY()]) {
            a5 = "visibilitychange";
            aQ()
        } else {
            emtj_startTime = new Date().getTime();
            a8 = new Date(emtj_startTime);
            a3 = emtj_getNowFormatDate(a8, 2);
            a4 = 0;
            bo = false;
            a9 = 10;
            bd = "in";
            a5 = "default";
            aV = [];
            bg = -1;
            bc = 0;
            a7 = l();
            bi(emtj_startTime)
        }
    }
};
var aC = [117016300211, 113300301472, 117001300541, 112101300783, 117003300159, 119303304274, 119093305971, 119309306421, 119094300302];
var p = false;
for (var L = 0; L < aC.length; L++) {
    if (emtj_pageId == aC[L]) {
        p = true
    }
}
if (af.indexOf("emwap.eastmoney.com/news/info/detail/") >= 0 || af.indexOf("stg-webjs-test.dfcfw.com/hsf10") >= 0 || af.indexOf("https://peh5.uufund.com") >= 0 || af.indexOf("https://www.uufund.com") >= 0 || p) {
    if (emtj_trueURL.indexOf("isTest=1&") < 0) {
        try {
            aO()
        } catch(ao) {}
    }
}
if (emtj_trueURL.indexOf("isTest=1") >= 1) {
    if (typeof(emtj_logSet) == "undefined" && ak) {
        ae()
    }
    if (typeof(emtj_logSet) != "undefined" && ah && ak) {
        ae()
    }
    if (typeof(emtj_logSet) != "undefined" && aG) {
        T()
    }
} else {
    if (typeof(emtj_logSet) == "undefined") {
        ae()
    }
    if (typeof(emtj_logSet) != "undefined" && ah) {
        ae()
    }
    if (typeof(emtj_logSet) != "undefined" && aG) {
        T()
    }
}
window.emtjLaunch = function(i) {
    emtj_pageId = i || emtj_pageId;
    emtj_creUserAcId();
    ap();
    ae()
};
window.bindPageTracker = function() {};
window.sendTrackLog = U;
window.sendRequestLog = P;
window.sendFirstScreenLog = aH;
while (send_arr.length) {
    var f = send_arr.shift();
    if (f[0] == "sendTrackLog") {
        U(f[1], f[2], f[3], f[4], f[5])
    } else {
        if (f[0] == "bindPageTracker") {} else {
            if (f[0] == "emtjLaunch") {
                emtj_creUserAcId();
                ap();
                ae()
            } else {
                if (f[0] == "sendRequestLog") {
                    P(f[1])
                } else {
                    if (f[0] == "sendFirstScreenLog") {
                        aH(f[1], f[2])
                    }
                }
            }
        }
    }
}
})(window);