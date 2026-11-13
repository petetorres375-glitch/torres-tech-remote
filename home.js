/* Torres Tech Remote home page behaviour: shared by EN, ES and PT. */
(function () {
  // Fade-in on scroll. Without JS (or IntersectionObserver) everything just shows.
  (function () {
    const els = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window)) { els.forEach((e) => e.classList.add("in")); return; }
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { threshold: 0.08 });
    els.forEach((e) => io.observe(e));
  })();
  // Android | iPhone switch for both how-to sections: guess the visitor's phone, one choice drives both.
  (function () {
    const ios = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
    const pick = (os) => {
      document.querySelectorAll(".os[data-os]").forEach((el) => { el.hidden = el.dataset.os !== os; });
      document.querySelectorAll("[data-pick]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.pick === os)));
    };
    // Phone language: Spanish and Portuguese (Brazil or Portugal) phones get videos and steps in their language.
    const STEPS = {
      es: {
        install: {
          android: ["Abra el navegador <b>Chrome</b> y escriba el enlace de su tarjeta.", "Baje y toque <b>Añadir a pantalla de inicio</b> en la tarjeta.", "Toque <b>Instalar</b>. El ícono de la tarjeta se agrega a su pantalla de inicio y a su lista de aplicaciones."],
          ios: ["Abra <b>Safari</b> y escriba el enlace de su tarjeta.", "Baje y toque <b>Añadir a pantalla de inicio</b> en la tarjeta.", "Toque <b>Compartir</b> (el cuadrado con una flecha).", "Toque <b>Añadir a pantalla de inicio</b> y luego <b>Añadir</b>."],
        },
        contact: {
          android: ["Abra su tarjeta.", "Toque el botón <b>Guardar contacto</b>.", "Descargue el archivo: toque <b>Descargar</b> en el cuadro que muestra el nombre del archivo (por ejemplo, <b>torres-tech-remote.vcf</b>) y dónde se guardará.", "Abra el archivo descargado.", "En la pantalla siguiente, toque <b>Importar</b> y elija dónde guardarlo.", "El contacto ya está en su lista de contactos."],
          ios: ["Abra <b>Safari</b> y escriba el enlace de su tarjeta.", "Baje y toque <b>Guardar contacto</b> en la tarjeta.", "Se abre el contacto. Toque <b>&#10003;</b> arriba a la izquierda."],
        },
      },
      pt: {
        install: {
          android: ["Abra o navegador <b>Chrome</b> e digite o link do seu cartão.", "Role para baixo e toque em <b>Adicionar à tela inicial</b> no cartão.", "Toque em <b>Instalar</b>. O ícone do cartão é adicionado à tela inicial e à lista de aplicativos."],
          ios: ["Abra o <b>Safari</b> e digite o link do seu cartão.", "Role para baixo e toque em <b>Adicionar à tela inicial</b> no cartão.", "Toque em <b>Compartilhar</b> (o quadrado com uma seta).", "Toque em <b>Adicionar à Tela de Início</b> e depois em <b>Adicionar</b>."],
        },
        contact: {
          android: ["Abra o seu cartão.", "Toque no botão <b>Salvar contato</b>.", "Baixe o arquivo: toque em <b>Baixar</b> na caixa que mostra o nome do arquivo (por exemplo, <b>torres-tech-remote.vcf</b>) e onde ele será salvo.", "Abra o arquivo baixado.", "Na próxima tela, toque em <b>Importar</b> e escolha onde salvar.", "O contato já está na sua lista de contatos."],
          ios: ["Abra o <b>Safari</b> e digite o link do seu cartão.", "Role para baixo e toque em <b>Salvar contato</b> no cartão.", "O contato abre. Toque em <b>&#10003;</b> no canto superior esquerdo."],
        },
      },
      "pt-PT": {
        install: {
          android: ["Abra o navegador <b>Chrome</b> e escreva a ligação do seu cartão.", "Desloque para baixo e toque em <b>Adicionar ao ecrã principal</b> no cartão.", "Toque em <b>Instalar</b>. O ícone do cartão é adicionado ao ecrã principal e à lista de aplicações."],
          ios: ["Abra o <b>Safari</b> e escreva a ligação do seu cartão.", "Desloque para baixo e toque em <b>Adicionar ao ecrã principal</b> no cartão.", "Toque em <b>Partilhar</b> (o quadrado com uma seta).", "Toque em <b>Adicionar ao ecrã principal</b> e depois em <b>Adicionar</b>."],
        },
        contact: {
          android: ["Abra o seu cartão.", "Toque no botão <b>Guardar contacto</b>.", "Transfira o ficheiro: toque em <b>Transferir</b> na caixa que mostra o nome do ficheiro (por exemplo, <b>torres-tech-remote.vcf</b>) e onde será guardado.", "Abra o ficheiro transferido.", "No ecrã seguinte, toque em <b>Importar</b> e escolha onde o guardar.", "O contacto já está na sua lista de contactos."],
          ios: ["Abra o <b>Safari</b> e escreva a ligação do seu cartão.", "Desloque para baixo e toque em <b>Guardar contacto</b> no cartão.", "O contacto abre. Toque em <b>&#10003;</b> no canto superior esquerdo."],
        },
      },
    };
    const lang = ((navigator.languages || [navigator.language]).map((l) => (l || "").toLowerCase())
      .map((l) => l === "pt-pt" ? "pt-PT" : l.slice(0, 2)).find((l) => ["en", "es", "pt", "pt-PT"].includes(l))) || "en";
    if (STEPS[lang]) {
      document.querySelectorAll(".os[data-os]").forEach((el) => {
        const clip = el.closest(".install").id === "install" ? "install" : "contact";
        const v = el.querySelector("video"), name = `/video/${clip}-${el.dataset.os}-${lang}`;
        v.src = name + ".mp4"; v.poster = name + ".webp";
        const ol = el.querySelector("ol");
        ol.lang = lang;
        ol.innerHTML = STEPS[lang][clip][el.dataset.os].map((li) => `<li>${li}</li>`).join("");
      });
    }
    document.documentElement.classList.add("js-os");
    pick(ios ? "ios" : "android");
    document.querySelectorAll("[data-pick]").forEach((b) => b.addEventListener("click", () => pick(b.dataset.pick)));
  })();
  // Install and Save contact videos: play only while on screen, tap to pause. Reduced motion: controls, no autoplay.
  (function () {
    const vids = document.querySelectorAll(".os-video video");
    if (matchMedia("(prefers-reduced-motion: reduce)").matches || !("IntersectionObserver" in window)) {
      vids.forEach((v) => { v.controls = true; v.preload = "metadata"; });
      return;
    }
    const paused = new WeakSet();
    const io = new IntersectionObserver((entries) => entries.forEach((e) => {
      if (e.isIntersecting && !paused.has(e.target)) e.target.play().catch(() => {});
      else e.target.pause();
    }), { threshold: 0.4 });
    vids.forEach((v) => {
      io.observe(v);
      v.addEventListener("click", () => {
        if (v.paused) { paused.delete(v); v.play().catch(() => {}); } else { paused.add(v); v.pause(); }
      });
    });
  })();
  // Featured-client screenshot carousels: each client is independent.
  (function () {
    const carousels = Array.from(document.querySelectorAll("[data-client-carousel]"));
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    carousels.forEach((carousel) => {
      const rail = carousel.querySelector(".shots");
      const slides = Array.from(rail.querySelectorAll("figure"));
      const dots = carousel.querySelector(".carousel-dots");
      const launch = carousel.querySelector(".shot-launch");
      let activeIndex = 0;
      let moving = false;
      let moveTimer;
      slides.forEach((slide, index) => {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "carousel-dot";
        dot.setAttribute("aria-label", `Show screenshot ${index + 1} of ${slides.length}`);
        dot.addEventListener("click", () => goTo(index));
        dots.appendChild(dot);
      });
      const dotButtons = Array.from(dots.querySelectorAll("button"));
      function updateDots() {
        dotButtons.forEach((dot, index) => dot.setAttribute("aria-current", String(index === activeIndex)));
      }
      function goTo(index) {
        activeIndex = Math.max(0, Math.min(slides.length - 1, index));
        const slide = slides[activeIndex];
        const left = slide.offsetLeft - (rail.clientWidth - slide.offsetWidth) / 2;
        moving = true;
        clearTimeout(moveTimer);
        moveTimer = setTimeout(() => { moving = false; }, reducedMotion ? 50 : 600);
        rail.scrollTo({ left: Math.max(0, left), behavior: reducedMotion ? "auto" : "smooth" });
        updateDots();
      }
      function open() {
        carousel.classList.add("is-open");
        if (!reducedMotion) {
          carousel.classList.remove("is-opening");
          void rail.offsetWidth;
          carousel.classList.add("is-opening");
        }
        goTo(activeIndex);
        carousel.querySelector("[data-close]").focus({ preventScroll: true });
      }
      function close() {
        carousel.classList.remove("is-open", "is-opening");
        activeIndex = 0;
        rail.scrollTo({ left: 0, behavior: "auto" });
        updateDots();
        launch.focus({ preventScroll: true });
      }
      launch.addEventListener("click", open);
      carousel.querySelector("[data-prev]").addEventListener("click", () => goTo((activeIndex - 1 + slides.length) % slides.length));
      carousel.querySelector("[data-next]").addEventListener("click", () => goTo((activeIndex + 1) % slides.length));
      carousel.querySelector("[data-close]").addEventListener("click", close);
      rail.addEventListener("scroll", () => {
        if (moving || !carousel.classList.contains("is-open")) return;
        const center = rail.scrollLeft + rail.clientWidth / 2;
        let closest = 0, distance = Infinity;
        slides.forEach((slide, index) => {
          const slideCenter = slide.offsetLeft + slide.offsetWidth / 2;
          const nextDistance = Math.abs(center - slideCenter);
          if (nextDistance < distance) { distance = nextDistance; closest = index; }
        });
        activeIndex = closest;
        updateDots();
      }, { passive: true });
      carousel.addEventListener("keydown", (event) => {
        if (!carousel.classList.contains("is-open")) return;
        if (event.key === "ArrowLeft") { event.preventDefault(); goTo((activeIndex - 1 + slides.length) % slides.length); }
        if (event.key === "ArrowRight") { event.preventDefault(); goTo((activeIndex + 1) % slides.length); }
        if (event.key === "Escape") { event.preventDefault(); close(); }
      });
      updateDots();
    });
  })();
})();
