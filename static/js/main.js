
"use strict";

document.addEventListener("DOMContentLoaded", () => {
    initMenu();
    initLightbox();
    initCatalog();
    initShowreel();
    initAppSchemeFallback();
});

function initAppSchemeFallback() {
 
    // Мапа "схема -> {ios, android}" сторінок у сторах.
    // За потреби легко додати нові схеми (tg, whatsapp тощо).
    const STORE_LINKS = {
        "viber:": {
            ios: "https://apps.apple.com/app/viber-messenger/id382617920",
            android: "https://play.google.com/store/apps/details?id=com.viber.voip"
        }
    };
 
    const FALLBACK_DELAY = 1500;
 
    const ua = navigator.userAgent;
    const isIOS = /iPhone|iPad|iPod/i.test(ua);
    const isAndroid = /Android/i.test(ua);
    const isMobile = isIOS || isAndroid;
 
    const links = [...document.querySelectorAll("a[href]")].filter(link => {
        try {
            return Object.prototype.hasOwnProperty.call(
                STORE_LINKS,
                new URL(link.href).protocol
            );
        } catch {
            return false;
        }
    });
 
    if (!links.length) return;
 
    links.forEach(link => {
 
        link.addEventListener("click", e => {
 
            let scheme;
 
            try {
                scheme = new URL(link.href).protocol;
            } catch {
                return;
            }
 
            const stores = STORE_LINKS[scheme];
 
            if (!stores) return;
 
            // На десктопі просто даємо браузеру спробувати відкрити
            // клієнт/веб-версію штатним чином — нічого не ламаємо.
            if (!isMobile) return;
 
            e.preventDefault();
 
            let didHide = false;
 
            const onVisibilityChange = () => {
                if (document.hidden) didHide = true;
            };
 
            document.addEventListener("visibilitychange", onVisibilityChange);
 
            window.location.href = link.href;
 
            setTimeout(() => {
 
                document.removeEventListener("visibilitychange", onVisibilityChange);
 
                if (didHide) return;
 
                window.location.href = isIOS ? stores.ios : stores.android;
 
            }, FALLBACK_DELAY);
 
        });
 
    });
 
}

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
    const lightbox = document.getElementById(
        "photoLightbox"
    );

    if (!lightbox) {
        return;
    }

    const image = lightbox.querySelector(
        ".photo-lightbox-image"
    );

    const closeButton = lightbox.querySelector(
        ".photo-lightbox-close"
    );

    const previousButton = lightbox.querySelector(
        ".photo-lightbox-prev"
    );

    const nextButton = lightbox.querySelector(
        ".photo-lightbox-next"
    );

    let currentTrigger = null;
    let touchStartX = 0;

    function getTriggers() {
        return [
            ...document.querySelectorAll(
                "[data-lightbox-src]"
            ),
        ].filter(trigger => {
            return trigger.offsetParent !== null;
        });
    }

    function getCurrentIndex() {
        return getTriggers().indexOf(currentTrigger);
    }

    function render(trigger) {
        if (!trigger || !image) {
            return;
        }

        currentTrigger = trigger;

        image.src = trigger.dataset.lightboxSrc;
        image.alt = trigger.dataset.lightboxAlt || "";
    }

    function open(trigger) {
        render(trigger);

        lightbox.hidden = false;

        document.body.classList.add(
            "lightbox-open"
        );

        closeButton?.focus();
    }

    function close() {
        lightbox.hidden = true;

        image?.removeAttribute("src");
        image?.removeAttribute("alt");

        document.body.classList.remove(
            "lightbox-open"
        );

        currentTrigger?.focus();
    }

    function showRelative(direction) {
        const triggers = getTriggers();

        if (!triggers.length) {
            return;
        }

        const currentIndex = getCurrentIndex();

        const nextIndex = (
            currentIndex +
            direction +
            triggers.length
        ) % triggers.length;

        render(triggers[nextIndex]);
    }

    function showPrevious() {
        showRelative(-1);
    }

    function showNext() {
        showRelative(1);
    }

    document.addEventListener("click", event => {
        const trigger = event.target.closest(
            "[data-lightbox-src]"
        );

        if (!trigger) {
            return;
        }

        if (
            event.target.closest(
                ".product-order-btn"
            )
        ) {
            return;
        }

        open(trigger);
    });

    document.addEventListener("keydown", event => {
        const trigger = event.target.closest(
            "[data-lightbox-src]"
        );

        if (
            trigger &&
            (
                event.key === "Enter" ||
                event.key === " "
            )
        ) {
            event.preventDefault();
            open(trigger);
            return;
        }

        if (lightbox.hidden) {
            return;
        }

        if (event.key === "Escape") {
            close();
        }

        if (event.key === "ArrowLeft") {
            showPrevious();
        }

        if (event.key === "ArrowRight") {
            showNext();
        }
    });

    closeButton?.addEventListener(
        "click",
        event => {
            event.stopPropagation();
            close();
        }
    );

    previousButton?.addEventListener(
        "click",
        event => {
            event.stopPropagation();
            showPrevious();
        }
    );

    nextButton?.addEventListener(
        "click",
        event => {
            event.stopPropagation();
            showNext();
        }
    );

    lightbox.addEventListener(
        "click",
        event => {
            if (event.target === lightbox) {
                close();
            }
        }
    );

    lightbox.addEventListener(
        "touchstart",
        event => {
            touchStartX =
                event.changedTouches[0].screenX;
        },
        {
            passive: true,
        }
    );

    lightbox.addEventListener(
        "touchend",
        event => {
            const touchEndX =
                event.changedTouches[0].screenX;

            const difference =
                touchEndX - touchStartX;

            if (Math.abs(difference) < 50) {
                return;
            }

            if (difference > 0) {
                showPrevious();
            } else {
                showNext();
            }
        },
        {
            passive: true,
        }
    );
}

function initCatalog() {
    const catalog = document.getElementById(
        "catalog"
    );

    const grid = document.getElementById(
        "catalogGrid"
    );

    const tabs = [
        ...document.querySelectorAll(
            "[data-catalog-tab]"
        ),
    ];

    const loadMoreButton =
        document.getElementById(
            "catalogLoadMore"
        );

    const priceAmount =
        document.querySelector(
            "#catalogPriceBlock .price-amount"
        );

    if (
        !catalog ||
        !grid ||
        !tabs.length
    ) {
        return;
    }

    const endpoint =
        catalog.dataset.catalogUrl;

    let currentCategory = "all";
    let nextPage = 2;
    let requestController = null;
    let isLoading = false;

    function setLoading(loading) {
        isLoading = loading;

        catalog.classList.toggle(
            "is-loading",
            loading
        );

        tabs.forEach(tab => {
            tab.disabled = loading;
        });

        if (loadMoreButton) {
            loadMoreButton.disabled = loading;
        }

        grid.setAttribute(
            "aria-busy",
            loading ? "true" : "false"
        );
    }

    function updateLoadMore({
        hasMore,
        remaining,
    }) {
        if (!loadMoreButton) {
            return;
        }

        loadMoreButton.hidden = !hasMore;

        if (!hasMore) {
            return;
        }

        const count = loadMoreButton.querySelector(
            ".catalog-toggle-count"
        );

        if (count) {
            count.textContent =
                remaining > 0
                    ? `+${remaining}`
                    : "";
        }
    }

    function updatePrice(tab) {
        if (!priceAmount) {
            return;
        }

        const price = tab.dataset.price;

        if (price) {
            priceAmount.textContent = price;
        }
    }

    async function loadItems({
        category,
        page,
        append,
    }) {
        if (isLoading && append) {
            return false;
        }

        requestController?.abort();

        requestController =
            new AbortController();

        setLoading(true);

        try {
            const params = new URLSearchParams({
                category,
                page: String(page),
            });

            const response = await fetch(
                `${endpoint}?${params}`,
                {
                    headers: {
                        "X-Requested-With":
                            "XMLHttpRequest",
                    },
                    signal:
                        requestController.signal,
                }
            );

            if (!response.ok) {
                throw new Error(
                    `HTTP ${response.status}`
                );
            }

            const data = await response.json();

            if (append) {
                grid.insertAdjacentHTML(
                    "beforeend",
                    data.html
                );
            } else {
                grid.innerHTML = data.html;
            }

            updateLoadMore({
                hasMore: data.has_more,
                remaining: data.remaining,
            });

            return true;
        } catch (error) {
            if (error.name === "AbortError") {
                return false;
            }

            console.error(
                "Catalog loading error:",
                error
            );

            if (!append) {
                grid.innerHTML = `
                    <div class="empty-state">
                        Не вдалося завантажити каталог.
                        Спробуйте ще раз.
                    </div>
                `;
            }

            return false;
        } finally {
            if (
                requestController &&
                !requestController.signal.aborted
            ) {
                setLoading(false);
            }
        }
    }

    async function activateTab(tab) {
        const category =
            tab.dataset.catalogTab;

        currentCategory = category;
        nextPage = 2;

        tabs.forEach(item => {
            const active = item === tab;

            item.classList.toggle(
                "active",
                active
            );

            item.setAttribute(
                "aria-selected",
                active ? "true" : "false"
            );

            item.tabIndex =
                active ? 0 : -1;
        });

        updatePrice(tab);

        await loadItems({
            category,
            page: 1,
            append: false,
        });
    }

    tabs.forEach((tab, index) => {
        tab.addEventListener(
            "click",
            () => activateTab(tab)
        );

        tab.addEventListener(
            "keydown",
            event => {
                if (
                    event.key !== "ArrowLeft" &&
                    event.key !== "ArrowRight"
                ) {
                    return;
                }

                event.preventDefault();

                const direction =
                    event.key === "ArrowRight"
                        ? 1
                        : -1;

                const nextIndex = (
                    index +
                    direction +
                    tabs.length
                ) % tabs.length;

                const nextTab =
                    tabs[nextIndex];

                nextTab.focus();
                activateTab(nextTab);
            }
        );
    });

    loadMoreButton?.addEventListener(
        "click",
        async () => {
            const loaded = await loadItems({
                category: currentCategory,
                page: nextPage,
                append: true,
            });

            if (loaded) {
                nextPage += 1;
            }
        }
    );
}


function initShowreel() {
    const cards = [
        ...document.querySelectorAll(
            "[data-showreel-card]"
        ),
    ];

    if (!cards.length) {
        return;
    }

    function prepareVideo(video) {
        if (video.dataset.loaded === "true") {
            return;
        }

        const source = video.querySelector(
            "source[data-src]"
        );

        if (!source) {
            return;
        }

        source.src = source.dataset.src;
        video.load();
        video.dataset.loaded = "true";
    }

    function pauseCard(card) {
        const video = card.querySelector(
            ".showreel-media"
        );

        if (!video) {
            return;
        }

        video.pause();
        video.controls = false;

        card.classList.remove(
            "is-playing"
        );
    }

    async function playCard(card) {
        cards.forEach(otherCard => {
            if (otherCard !== card) {
                pauseCard(otherCard);
            }
        });

        const video = card.querySelector(
            ".showreel-media"
        );

        if (!video) {
            return;
        }

        prepareVideo(video);

        card.classList.add(
            "is-loading"
        );

        try {
            video.controls = true;

            await video.play();

            card.classList.add(
                "is-playing"
            );
        } catch (error) {
            console.error(
                "Video playback error:",
                error
            );

            video.controls = false;

            card.classList.remove(
                "is-playing"
            );
        } finally {
            card.classList.remove(
                "is-loading"
            );
        }
    }

    cards.forEach(card => {
        const video = card.querySelector(
            ".showreel-media"
        );

        const playButton = card.querySelector(
            ".showreel-play-btn"
        );

        if (!video || !playButton) {
            return;
        }

        playButton.addEventListener(
            "click",
            () => {
                playCard(card);
            }
        );

        video.addEventListener(
            "ended",
            () => {
                video.currentTime = 0;
                video.controls = false;

                card.classList.remove(
                    "is-playing"
                );
            }
        );

        video.addEventListener(
            "error",
            () => {
                video.controls = false;

                card.classList.remove(
                    "is-loading",
                    "is-playing"
                );
            }
        );
    });
}