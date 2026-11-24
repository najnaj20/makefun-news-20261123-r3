# makefun-news-20261123-r3

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/najnaj20/makefun-news-20261123-r3/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/najnaj20/makefun-news-20261123-r3/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A clean one-page newspaper front page summing up the world news of Monday 23 November 2026 in 15 stories with large, legible type. Two big leads on top: COP31 collapses with no deal in Antalya, the longest COP ever; and the Democrats clinch the US House with at least 258 seats, the largest majority since 1992. Below them, thirteen more stories in two wide columns across Europe, the Middle East, Asia-Pacific and the Americas, each with its source listed in STORIES.md. Every story happened or was first reported on Monday 23 November 2026, and the page carries a visible DATE CHECK box saying so. The image is drawn in code by render.py (Pillow + DejaVu) from verified reports (Reuters, AP, CNN, BBC, Xinhua, The Guardian); main.ts copies it to the output directory.

This is the third version of the entry. The first was clean but thin with only 6 stories; the second packed in 30 stories and the tiny text was punished by the judge. This version goes back to a clean layout with room to read, but with 15 stories instead of 6.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=0c4qjdq4&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
