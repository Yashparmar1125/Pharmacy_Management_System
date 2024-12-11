"use strict";
! function(i, l) {
    var n = l(window),
        o = l("body"),
        s = i.Break,
        c = l(".chat-profile-toggle"),
        h = l(".nk-chat-profile"),
        d = l(".nk-chat-body"),
        r = l(".nk-chat-aside"),
        C = l(".chat-open"),
        v = l(".nk-chat-hide"),
        u = l(".chat-search-toggle"),
        f = l(".nk-chat-head-search"),
        m = "nk-chat-profile-overlay",
        p = "profile-shown",
        w = "chat-profile-autohide",
        g = "hide-aside",
        k = "show-chat",
        W = 9999,
        b = s.lg;
    i.Chats = function() {
        function a() {
            i.Win.width >= b ? o.hasClass(w) || o.addClass(w) : o.hasClass(w) && o.removeClass(w)
        }

        function s(s) {
            c.addClass("active"), h.addClass("visible"), d.addClass(p), !0 === s && o.addClass("chat-" + p)
        }

        function e(s) {
            c.removeClass("active"), h.removeClass("visible"), d.removeClass(p), !0 === s && o.removeClass("chat-" + p)
        }

        function t() {
            var s = "." + m;
            i.Win.width < W && h.hasClass("visible") ? h.next().hasClass(m) || h.after('<div class="' + m + '"></div>') : l(s).remove(), l(s).on("click", function() {
                l(this).remove(), e(!0), a()
            })
        }
        u.on("click", function(s) {
            i.Win.width <= W && (e(), t()), f.addClass("show-search"), s.preventDefault()
        }), l(document).on("mouseup", function(s) {
            f.is(s.target) || 0 !== f.has(s.target).length || f.find(".form-control").val() || f.removeClass("show-search")
        }), C.on("click", function(s) {
            C.parent().removeClass("current"), r.addClass(g), d.addClass(k), l(this).parent().addClass("current"), s.preventDefault()
        }), v.on("click", function() {
            r.removeClass(g), d.removeClass(k)
        }), c.on("click", function(s) {
            c.toggleClass("active"), h.toggleClass("visible"), d.toggleClass(p), l(this).hasClass("active") && !o.hasClass("chat-" + p) ? o.addClass("chat-" + p) : o.removeClass("chat-" + p), i.Win.width >= b && (o.hasClass(w) ? o.removeClass(w) : i.Win.width < W && !l(this).hasClass("active") && o.addClass(w)), t(), s.preventDefault()
        }), (i.Win.width >= W ? s : e)(), a(), n.on("resize", function() {
            o.hasClass(w) && (i.Win.width >= W ? s : e)(), i.Win.width >= b && i.Win.width < W && o.hasClass("chat-" + p) && (o.removeClass("chat-" + p), e()), t()
        })
    }, i.coms.docReady.push(i.Chats)
}(NioApp, jQuery);