const $ = (id) => document.getElementById(id);
const repo = "https://github.com/jkf87/conan-astracar";
const media = (s, ext) => `media/${encodeURIComponent(s.slug)}.${ext}`;
const screening = (s) => `films.html?style=${encodeURIComponent(s.slug)}`;
const normalize = (s) => s.normalize("NFKC").toLocaleLowerCase().trim();
const element = (tag, text, cls) => {
  const e = document.createElement(tag);
  if (text !== undefined) e.textContent = text;
  if (cls) e.className = cls;
  return e;
};

function card(s) {
  const link = element("a", undefined, "card");
  link.href = screening(s);
  const thumb = element("span", undefined, "card-thumb");
  const img = element("img");
  img.loading = "lazy";
  img.alt = "";
  img.src = media(s, "jpg");
  thumb.append(img, element("small", `${s.seconds.toFixed(0)}초`));
  link.append(
    thumb,
    element("small", `${s.number} / ${s.category}`, "card-kicker"),
    element("h3", s.nameKo),
    element("p", s.titleKo),
  );
  return link;
}

function home(styles) {
  const dialog = $("trailer-dialog"),
    trailer = $("trailer-player");
  $("trailer-open").onclick = () => {
    dialog.showModal();
    if (!trailer.getAttribute("src")) trailer.src = "trailer.mp4";
    trailer.play().catch(() => {});
  };
  $("trailer-close").onclick = () => dialog.close();
  dialog.addEventListener("close", () => trailer.pause());
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
  const search = $("search"),
    category = $("category");
  for (const c of new Set(styles.map((s) => s.category)))
    category.add(new Option(c, c));
  const params = new URLSearchParams(location.search);
  search.value = params.get("q") || "";
  category.value = params.get("category") || "";
  const refresh = () => {
    const term = normalize(search.value);
    const rows = styles.filter(
      (s) =>
        (!category.value || s.category === category.value) &&
        normalize(
          [
            s.nameKo,
            s.nameEn,
            s.titleKo,
            s.slug,
            s.category,
            s.number,
            s.storyKo,
          ].join(" "),
        ).includes(term),
    );
    $("count").textContent = `${rows.length}편 / 전체 ${styles.length}편`;
    $("cards").replaceChildren(...rows.map(card));
    if (!rows.length)
      $("cards").append(
        element(
          "p",
          "검색 결과가 없습니다. 다른 검색어나 분류를 골라 보세요.",
          "empty",
        ),
      );
    const url = new URL(location.href);
    for (const [key, value] of [
      ["q", search.value],
      ["category", category.value],
    ]) {
      if (value) url.searchParams.set(key, value);
      else url.searchParams.delete(key);
    }
    history.replaceState(null, "", url);
  };
  search.addEventListener("input", refresh);
  category.addEventListener("change", refresh);
  refresh();
  const featured = [
    "text-flash-cuts",
    "ukiyoe",
    "pixel-rpg",
    "neon-tubes",
    "paper-popup",
    "teardown",
  ].map((slug) => styles.find((s) => s.slug === slug));
  let active = 0;
  const feature = (i) => {
    active = (i + featured.length) % featured.length;
    const s = featured[active];
    $("feature-img").src = media(s, "jpg");
    $("feature-title").textContent = s.titleKo;
    $("feature-kind").textContent = `${s.number} / ${s.nameKo}`;
    $("feature-link").href = screening(s);
    $("feature-page").textContent = `${active + 1} / ${featured.length}`;
  };
  $("prev").onclick = () => feature(active - 1);
  $("next").onclick = () => feature(active + 1);
  feature(0);
}

async function copy(text, notice) {
  const input = $("manual-copy");
  try {
    await navigator.clipboard.writeText(text);
    input.hidden = true;
    $("feedback").textContent = notice;
  } catch {
    input.hidden = false;
    input.value = text;
    input.focus();
    input.select();
    $("feedback").textContent = "선택된 텍스트를 복사하세요.";
  }
}

function theater(styles) {
  const select = $("film-select"),
    original = $("original"),
    astra = $("astra");
  let selected;
  let paired = false;
  let priorMute = false;
  const compare = $("compare");
  function stopPair() {
    if (!paired) return;
    paired = false;
    astra.pause();
    original.pause();
    original.muted = priorMute;
    compare.textContent = "두 영상 함께 재생";
    compare.setAttribute("aria-pressed", "false");
  }
  compare.onclick = async () => {
    if (paired) {
      stopPair();
      return;
    }
    paired = true;
    priorMute = original.muted;
    original.muted = true;
    compare.textContent = "함께 재생 멈추기";
    compare.setAttribute("aria-pressed", "true");
    $("feedback").textContent =
      "두 영상을 처음부터 재생합니다. 원작 소리는 플레이어에서 켤 수 있습니다.";
    try {
      astra.currentTime = 0;
      original.currentTime = 0;
      await Promise.all([astra.play(), original.play()]);
    } catch {
      if (paired) {
        stopPair();
        $("feedback").textContent =
          "함께 재생을 시작하지 못했습니다. 각 플레이어의 재생 버튼을 눌러 주세요.";
      }
    }
  };
  let group;
  for (const s of styles) {
    if (group?.label !== s.category) {
      group = document.createElement("optgroup");
      group.label = s.category;
      select.append(group);
    }
    group.append(
      new Option(`${s.number} · ${s.nameKo} — ${s.titleKo}`, s.slug),
    );
  }
  const screen = (slug, push = false) => {
    const s = styles.find((row) => row.slug === slug) || styles[0];
    stopPair();
    selected = styles.indexOf(s);
    select.value = s.slug;
    astra.pause();
    original.pause();
    astra.poster = media(s, "jpg");
    astra.src = media(s, "mp4");
    original.poster = s.originalPoster;
    original.src = s.originalVideo;
    $("style-name").textContent = s.nameKo;
    $("category-name").textContent = `${s.category} / ${s.nameEn}`;
    $("astra-title").textContent = s.titleKo;
    $("original-title").textContent = s.originalTitle;
    $("credit").textContent =
      `Lemo-Opuscar by Lemomo (LemoLab)${s.originalAuthor.startsWith("Lemomo") ? "" : " · 스타일 기여 " + s.originalAuthor}`;
    $("story").textContent = s.storyKo;
    $("technique").textContent = s.techniqueKo;
    $("original-link").href = s.originalPage;
    $("guide").href = s.guide;
    $("source").href = `${repo}/blob/main/${s.source}`;
    $("film-position").textContent = `${selected + 1} / ${styles.length}`;
    $("feedback").textContent = "";
    $("manual-copy").hidden = true;
    document.title = `${s.nameKo} · ${s.titleKo} | 아스트라카 상영관`;
    if (push) history.pushState(null, "", screening(s));
    $("copy-link").onclick = () =>
      copy(
        new URL(screening(s), location.href).href,
        "이 작품의 상영관 링크를 복사했습니다.",
      );
    $("copy-prompt").onclick = () =>
      copy(
        `$lemo-opuscar ${s.nameEn} (${s.slug}) 스타일로 “[내 주제]”에 대한 한국어 단편을 만들어 줘. 아래 스타일 가이드를 참고해 새 이야기와 장면을 구성하고, 실행 가능한 소스와 MP4를 함께 만들어 줘.\n${s.guide}`,
        "제작 프롬프트를 복사했습니다. [내 주제]를 바꿔 Codex에 붙여 넣으세요.",
      );
  };
  const fromURL = () =>
    screen(new URLSearchParams(location.search).get("style"));
  select.onchange = () => screen(select.value, true);
  const step = (delta) =>
    screen(
      styles[(selected + delta + styles.length) % styles.length].slug,
      true,
    );
  $("film-prev").onclick = () => step(-1);
  $("film-next").onclick = () => step(1);
  for (const [player, other] of [
    [astra, original],
    [original, astra],
  ]) {
    player.addEventListener("play", () => {
      if (!paired) other.pause();
    });
    player.addEventListener("ended", () => {
      if (paired && other.ended) stopPair();
    });
  }
  window.addEventListener("popstate", fromURL);
  fromURL();
}

try {
  const response = await fetch("catalog.json");
  if (!response.ok) throw Error(response.statusText);
  const styles = await response.json();
  if (document.body.dataset.page === "home") home(styles);
  else theater(styles);
} catch {
  const status = $("count") || $("feedback");
  status.textContent =
    "작품 목록을 불러오지 못했습니다. 페이지를 새로 고쳐 주세요.";
}
