
"use strict";

document.addEventListener("DOMContentLoaded", () => {
    initMenu();
    initLightbox();
    initCatalog();
    initShowreel();
});

function initMenu() {

    const burgerBtn = document.getElementById("burgerBtn");
    const mobileNav = document.getElementById("mobileNav");
    const closeNav = document.getElementById("closeNav");

    if (!burgerBtn || !mobileNav || !closeNav) {
        return;
    }

    const openMenu = () => {
        mobileNav.hidden = false;
        document.body.classList.add("menu-open");
    };

    const closeMenu = () => {
        mobileNav.hidden = true;
        document.body.classList.remove("menu-open");
    };

    burgerBtn.addEventListener("click", openMenu);

    closeNav.addEventListener("click", closeMenu);

    mobileNav.addEventListener("click", (e) => {
        if (e.target === mobileNav) {
            closeMenu();
        }
    });

    mobileNav.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && !mobileNav.hidden) {
            closeMenu();
        }
    });

}

function initLightbox() {

    const triggers = [...document.querySelectorAll("[data-lightbox-src]")];
    const lightbox = document.getElementById("photoLightbox");

    if (!triggers.length || !lightbox) return;

    const image = lightbox.querySelector(".photo-lightbox-image");
    const closeBtn = lightbox.querySelector(".photo-lightbox-close");
    const prevBtn = lightbox.querySelector(".photo-lightbox-prev");
    const nextBtn = lightbox.querySelector(".photo-lightbox-next");

    let current = 0;
    let touchStart = 0;

    function render(index) {

        current = (index + triggers.length) % triggers.length;

        const trigger = triggers[current];

        image.src = trigger.dataset.lightboxSrc;
        image.alt = trigger.dataset.lightboxAlt || "";

    }

    function open(index) {

        render(index);

        lightbox.hidden = false;
        document.body.classList.add("lightbox-open");

    }

    function close() {

        lightbox.hidden = true;

        image.removeAttribute("src");
        image.removeAttribute("alt");

        document.body.classList.remove("lightbox-open");

    }

    function prev() {
        render(current - 1);
    }

    function next() {
        render(current + 1);
    }

    triggers.forEach((trigger, index) => {
        trigger.addEventListener("click", () => open(index));
    });

    closeBtn.addEventListener("click", e => {
        e.stopPropagation();
        close();
    });

    prevBtn.addEventListener("click", e => {
        e.stopPropagation();
        prev();
    });

    nextBtn.addEventListener("click", e => {
        e.stopPropagation();
        next();
    });

    lightbox.addEventListener("click", e => {

        if (e.target === lightbox) {
            close();
        }

    });

    document.addEventListener("keydown", e => {

        if (lightbox.hidden) return;

        switch (e.key) {

            case "Escape":
                close();
                break;

            case "ArrowLeft":
                prev();
                break;

            case "ArrowRight":
                next();
                break;

        }

    });

    lightbox.addEventListener("touchstart", e => {
        touchStart = e.changedTouches[0].screenX;
    });

    lightbox.addEventListener("touchend", e => {

        const diff = e.changedTouches[0].screenX - touchStart;

        if (Math.abs(diff) < 50) return;

        diff > 0 ? prev() : next();

    });

}

function initCatalog() {

    const catalog = document.getElementById("catalog");
    const tabs = [...document.querySelectorAll("[data-catalog-tab]")];
    const panels = [...document.querySelectorAll("[data-catalog-panel]")];

    const VISIBLE_LIMIT = 10;

    if (!tabs.length || !panels.length) return;

    function updatePanel(panel) {

        const items = [...panel.querySelectorAll("[data-catalog-item]")];
        const toggle = panel.querySelector("[data-catalog-toggle]");

        if (!toggle) return;

        const expanded = panel.classList.contains("expanded");

        items.forEach((item, index) => {
            item.hidden = !expanded && index >= VISIBLE_LIMIT;
        });

        if (items.length <= VISIBLE_LIMIT) {
            toggle.hidden = true;
            return;
        }

        toggle.hidden = false;
        toggle.classList.toggle("is-expanded", expanded);

        const hiddenCount = items.length - VISIBLE_LIMIT;

        toggle.innerHTML = expanded
            ? "<span>Показати менше</span>"
            : `
                <span>Дивитись більше</span>
                <span class="catalog-toggle-count">
                    +${hiddenCount}
                </span>
            `;
    }

    function resetPanel(panel) {

        panel.classList.remove("expanded");

        updatePanel(panel);

    }

    function activateTab(id) {

        tabs.forEach(tab => {

            const active = tab.dataset.catalogTab === id;

            tab.classList.toggle("active", active);
            tab.setAttribute("aria-selected", active ? "true" : "false");
            tab.tabIndex = active ? 0 : -1;

        });

        panels.forEach(panel => {

            const active = panel.dataset.catalogPanel === id;

            panel.hidden = !active;

            if (active) {
                resetPanel(panel);
            }

        });

    }

    panels.forEach(panel => {

        const toggle = panel.querySelector("[data-catalog-toggle]");

        if (!toggle) return;

        let busy = false;

        toggle.addEventListener("click", async () => {

            if (busy) return;

            busy = true;

            toggle.disabled = true;

            panel.classList.toggle("expanded");

            updatePanel(panel);

            if (!panel.classList.contains("expanded") && catalog) {

                catalog.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

                await new Promise(r => setTimeout(r, 500));

            }

            toggle.disabled = false;

            busy = false;

        });

    });

    tabs.forEach((tab, index) => {

        tab.addEventListener("click", () => {
            activateTab(tab.dataset.catalogTab);
        });

        tab.addEventListener("keydown", e => {

            if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") {
                return;
            }

            e.preventDefault();

            const next =
                e.key === "ArrowRight"
                    ? (index + 1) % tabs.length
                    : (index - 1 + tabs.length) % tabs.length;

            tabs[next].focus();

            activateTab(tabs[next].dataset.catalogTab);

        });

    });

    activateTab(
        document.querySelector("[data-catalog-tab].active")?.dataset.catalogTab ??
        tabs[0].dataset.catalogTab
    );

}


function initShowreel() {

    const cards = [...document.querySelectorAll("[data-showreel-card]")];

    if (!cards.length) return;

    function pauseCard(card) {

        const video = card.querySelector(".showreel-media");

        if (!video) return;

        video.pause();
        video.currentTime = 0;
        video.controls = false;

        card.classList.remove("is-playing");

    }

    function playCard(card) {

        cards.forEach(otherCard => {
            if (otherCard !== card) {
                pauseCard(otherCard);
            }
        });

        const video = card.querySelector(".showreel-media");

        if (!video) return;

        card.classList.add("is-playing");
        video.controls = true;

        video.play().catch(() => {
            pauseCard(card);
        });

    }

    cards.forEach(card => {

        const video = card.querySelector(".showreel-media");
        const playBtn = card.querySelector(".showreel-play-btn");

        if (!video || !playBtn) return;

        playBtn.addEventListener("click", () => playCard(card));

        video.addEventListener("ended", () => {
            pauseCard(card);
        });

        video.addEventListener("pause", () => {

            if (video.currentTime === 0 || video.ended) {
                card.classList.remove("is-playing");
            }

        });

    });

}