document.addEventListener("DOMContentLoaded", () => {

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

    closeButton.addEventListener("click", (event) => {
        event.stopPropagation();
        closeLightbox();
    });

    prevButton.addEventListener("click", (event) => {
        event.stopPropagation();
        showPrev();
    });

    nextButton.addEventListener("click", (event) => {
        event.stopPropagation();
        showNext();
    });

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

document.addEventListener("DOMContentLoaded", () => {
    const catalog = document.getElementById("catalog");
    const catalogTabs = Array.from(document.querySelectorAll("[data-catalog-tab]"));
    const catalogPanels = Array.from(document.querySelectorAll("[data-catalog-panel]"));
    const visibleLimit = 10;

    if (!catalogTabs.length || !catalogPanels.length) {
        return;
    }

    const updateCatalogPanel = (panel) => {
        const items = Array.from(panel.querySelectorAll("[data-catalog-item]"));
        const toggle = panel.querySelector("[data-catalog-toggle]");
        const isExpanded = panel.dataset.expanded === "true";
        const hiddenCount = Math.max(items.length - visibleLimit, 0);

        if (!toggle || !items.length) {
            return;
        }

        items.forEach((item, index) => {
            item.hidden = !isExpanded && index >= visibleLimit;
        });

        if (items.length <= visibleLimit) {
            toggle.hidden = true;
            toggle.classList.remove("is-expanded");
            return;
        }

        toggle.hidden = false;
        toggle.classList.toggle("is-expanded", isExpanded);

        if (isExpanded) {
            toggle.innerHTML = `<span>Показати менше</span>`;
        } else {
            toggle.innerHTML = `
                <span>Дивитись більше</span>
                <span class="catalog-toggle-count">+${hiddenCount}</span>
            `;
        }
    };

    const resetPanel = (panel) => {
        panel.dataset.expanded = "false";
        updateCatalogPanel(panel);
    };

    const activateCatalogTab = (selectedId) => {
        catalogTabs.forEach((tab) => {
            const isActive = tab.dataset.catalogTab === selectedId;

            tab.classList.toggle("active", isActive);
            tab.setAttribute("aria-selected", isActive ? "true" : "false");
            tab.setAttribute("tabindex", isActive ? "0" : "-1");
        });

        catalogPanels.forEach((panel) => {
            const isActive = panel.dataset.catalogPanel === selectedId;

            panel.hidden = !isActive;

            if (isActive) {
                resetPanel(panel);
            }
        });
    };

    catalogPanels.forEach((panel) => {
        const toggle = panel.querySelector("[data-catalog-toggle]");

        if (!toggle) {
            return;
        }

        toggle.addEventListener("click", () => {
            const isExpanded = panel.dataset.expanded === "true";

            if (isExpanded) {
                panel.dataset.expanded = "false";
                updateCatalogPanel(panel);

                if (catalog) {
                    catalog.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                }

                return;
            }

            panel.dataset.expanded = "true";
            updateCatalogPanel(panel);
        });
    });

    catalogTabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            activateCatalogTab(tab.dataset.catalogTab);
        });

        tab.addEventListener("keydown", (event) => {
            const currentIndex = catalogTabs.indexOf(tab);

            if (event.key === "ArrowRight") {
                event.preventDefault();
                const nextTab = catalogTabs[currentIndex + 1] || catalogTabs[0];
                nextTab.focus();
                activateCatalogTab(nextTab.dataset.catalogTab);
            }

            if (event.key === "ArrowLeft") {
                event.preventDefault();
                const prevTab = catalogTabs[currentIndex - 1] || catalogTabs[catalogTabs.length - 1];
                prevTab.focus();
                activateCatalogTab(prevTab.dataset.catalogTab);
            }
        });
    });

    const activeTab = document.querySelector("[data-catalog-tab].active") || catalogTabs[0];

    if (activeTab) {
        activateCatalogTab(activeTab.dataset.catalogTab);
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const showreel = document.querySelector(".showreel-video");

    if (!showreel) {
        return;
    }

    const card = showreel.querySelector(".showreel-card");
    const videos = Array.from(showreel.querySelectorAll("[data-showreel-video]"));
    const thumbs = Array.from(showreel.querySelectorAll("[data-showreel-thumb]"));
    const playButton = showreel.querySelector(".showreel-play-btn");

    if (!card || !videos.length || !playButton) {
        return;
    }

    let activeIndex = 0;

    const getActiveVideo = () => videos[activeIndex];

    const pauseAllVideos = () => {
        videos.forEach((video) => {
            video.pause();
            video.controls = false;
            video.currentTime = 0;
        });

        card.classList.remove("is-playing");
    };

    const activateVideo = (index) => {
        pauseAllVideos();

        activeIndex = index;

        videos.forEach((video, videoIndex) => {
            const isActive = videoIndex === activeIndex;
            video.hidden = !isActive;
            video.classList.toggle("active", isActive);
        });

        thumbs.forEach((thumb, thumbIndex) => {
            thumb.classList.toggle("active", thumbIndex === activeIndex);
        });
    };

    const playActiveVideo = () => {
        const video = getActiveVideo();

        if (!video) {
            return;
        }

        card.classList.add("is-playing");
        video.controls = true;

        const playPromise = video.play();

        if (playPromise !== undefined) {
            playPromise.catch(() => {
                card.classList.remove("is-playing");
                video.controls = false;
            });
        }
    };

    thumbs.forEach((thumb) => {
        thumb.addEventListener("click", () => {
            const index = Number(thumb.dataset.showreelThumb);
            activateVideo(index);
        });
    });

    playButton.addEventListener("click", playActiveVideo);

    videos.forEach((video) => {
        video.addEventListener("ended", () => {
            card.classList.remove("is-playing");
            video.controls = false;
            video.currentTime = 0;
        });
    });

    activateVideo(0);
});