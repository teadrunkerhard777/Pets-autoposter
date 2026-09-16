# Media policy

Use the lead image supplied by the attributed source when its remote URL passes
the shared image validation. If no usable source image exists, use only the
project-owned generated cover assigned to the post category. A category cover
is presentation, not a depiction of the reported event. Do not download images
from blocked pages or use images with unclear publication rights.

During `DRY_RUN`, each selected remote image is downloaded once only for
validation and immediately removed. A missing or rejected remote image falls
back to the category cover; if that cover is unavailable, the post falls back
to text.

When an RSS entry contains article text but no image, only the selected article
page is fetched to recover its lead image. Known site logos are rejected by an
exact source-specific rule and fall back to a project cover.

The separate video schedule uses only MP4 files returned by the official
Pexels and Pixabay APIs. Every video caption includes only a compact source
link, without a separate creator byline. Candidate files are limited to 40
seconds and 49 MiB, downloaded once to the system temp directory, validated,
uploaded to Telegram, and always removed locally. Video history is written only
after Telegram confirms success.
