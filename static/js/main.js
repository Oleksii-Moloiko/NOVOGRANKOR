document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll("[data-catalog-tab]");
    const panels = document.querySelectorAll("[data-catalog-panel]");

    if (tabs.length && panels.length) {
        tabs.forEach((tab) => {
            tab.addEventListener("click", () => {
                const targetId = tab.dataset.catalogTab;

                tabs.forEach((item) => {
                    item.classList.remove("active");
                    item.setAttribute("aria-selected", "false");
                });

                panels.forEach((panel) => {
                    panel.hidden = panel.dataset.catalogPanel !== targetId;
                });

                tab.classList.add("active");
                tab.setAttribute("aria-selected", "true");
            });
        });
    }

    const burgerBtn = document.getElementById("burgerBtn");
    const mobileNav = document.getElementById("mobileNav");
    const closeNav = document.getElementById("closeNav");

    if (burgerBtn && mobileNav && closeNav) {
        const openMenu = () => {
            mobileNav.hidden = false;
        };

        const closeMenu = () => {
            mobileNav.hidden = true;
        };

        burgerBtn.addEventListener("click", openMenu);
        closeNav.addEventListener("click", closeMenu);

        mobileNav.addEventListener("click", (event) => {
            if (event.target === mobileNav) {
                closeMenu();
            }
        });

        mobileNav.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", closeMenu);
        });
    }

    const triggers = Array.from(document.querySelectorAll("[data-lightbox-src]"));
    const lightbox = document.getElementById("photoLightbox");

    if (!triggers.length || !lightbox) {
        return;
    }

    const image = lightbox.querySelector(".photo-lightbox-image");
    const closeButton = lightbox.querySelector(".photo-lightbox-close");
    const prevButton = lightbox.querySelector(".photo-lightbox-prev");
    const nextButton = lightbox.querySelector(".photo-lightbox-next");

    let currentIndex = 0;
    let touchStartX = 0;

    const openLightbox = (index) => {
        currentIndex = index;
        const trigger = triggers[currentIndex];

        image.src = trigger.dataset.lightboxSrc;
        image.alt = trigger.dataset.lightboxAlt || "";

        lightbox.hidden = false;
        document.body.classList.add("lightbox-open");
    };

    const closeLightbox = () => {
        lightbox.hidden = true;
        image.src = "";
        image.alt = "";
        document.body.classList.remove("lightbox-open");
    };

    const showPrev = () => {
        currentIndex = (currentIndex - 1 + triggers.length) % triggers.length;
        openLightbox(currentIndex);
    };

    const showNext = () => {
        currentIndex = (currentIndex + 1) % triggers.length;
        openLightbox(currentIndex);
    };

    triggers.forEach((trigger, index) => {
        trigger.addEventListener("click", () => openLightbox(index));
    });

    closeButton.addEventListener("click", closeLightbox);
    prevButton.addEventListener("click", showPrev);
    nextButton.addEventListener("click", showNext);

    lightbox.addEventListener("click", (event) => {
        if (event.target === lightbox) {
            closeLightbox();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (lightbox.hidden) {
            return;
        }

        if (event.key === "Escape") {
            closeLightbox();
        }

        if (event.key === "ArrowLeft") {
            showPrev();
        }

        if (event.key === "ArrowRight") {
            showNext();
        }
    });

    lightbox.addEventListener("touchstart", (event) => {
        touchStartX = event.changedTouches[0].screenX;
    });

    lightbox.addEventListener("touchend", (event) => {
        const touchEndX = event.changedTouches[0].screenX;
        const diff = touchEndX - touchStartX;

        if (Math.abs(diff) < 50) {
            return;
        }

        if (diff > 0) {
            showPrev();
        } else {
            showNext();
        }
    });
});