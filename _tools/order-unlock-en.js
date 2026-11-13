  // The pay box is folded; open it for #order links (FAQ, old emails with #order).
  (function () {
    const box = document.getElementById("order");
    const open = () => { box.open = true; };
    if (location.hash === "#order") open();
    window.addEventListener("hashchange", () => { if (location.hash === "#order") open(); });
    document.querySelectorAll("[data-open-order]").forEach((a) => a.addEventListener("click", open));
  })();
  (function () {
    const form = document.getElementById("order-unlock");
    const msg = document.getElementById("order-msg");
    const enc = new TextEncoder();
    const bytes = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));
    async function unlock(code) {
      const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", enc.encode("ttr-order:" + code)));
      const h = digest[0].toString(16).padStart(2, "0");
      const base = await crypto.subtle.importKey("raw", enc.encode(code), "PBKDF2", false, ["deriveKey"]);
      for (const lock of ORDER_LOCKS.filter((l) => l.h === h)) {
        const key = await crypto.subtle.deriveKey(
          { name: "PBKDF2", salt: bytes(lock.salt), iterations: 250000, hash: "SHA-256" },
          base, { name: "AES-GCM", length: 256 }, false, ["decrypt"]);
        try {
          const plain = await crypto.subtle.decrypt({ name: "AES-GCM", iv: bytes(lock.iv) }, key, bytes(lock.data));
          return JSON.parse(new TextDecoder().decode(plain));
        } catch (err) { /* another code with the same hint; keep looking */ }
      }
      throw new Error("no match");
    }
    // client_reference_id tells Pedro in Stripe which customer's code paid.
    const withRef = (url, code) => url + (url.includes("?") ? "&" : "?") + "client_reference_id=" + code;
    async function tryCode(code) {
      msg.className = "order-msg"; msg.textContent = "Checking…";
      try {
        const links = await unlock(code);
        document.getElementById("order-monthly").href = withRef(links.monthly, code);
        document.getElementById("order-yearly").href = withRef(links.yearly, code);
        document.getElementById("order-pay").hidden = false;
        document.getElementById("order-ready").hidden = false;
        document.getElementById("order-intro").hidden = true;
        form.hidden = true;
      } catch (err) {
        msg.className = "order-msg bad";
        msg.textContent = (window.crypto && crypto.subtle)
          ? "That code doesn’t match. Check the code we sent with your preview."
          : "This browser can’t unlock the links. Email us for your payment link.";
      }
    }
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      tryCode(form.code.value.toUpperCase().replace(/\s+/g, ""));
    });
    // "Make it live" link sent with the preview: torrestechremote.com/live#CODE lands here as #pay=CODE
    // (after the #, so the code never reaches server logs or analytics).
    const linked = location.hash.match(/^#pay=([A-Za-z2-9]{6})$/);
    if (linked) {
      const order = document.getElementById("order");
      order.open = true;
      form.code.value = linked[1].toUpperCase();
      order.scrollIntoView();
      tryCode(form.code.value);
    }
  })();
