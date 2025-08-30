from muxtools import *
episode = int(input("Please enter an episode number: "))
setup = Setup(
    f"{episode:02d}",
     None,
    bdmv_dir=f"./BDMV/",
    show_name="PriPara",
    out_name=R"$show$ - E$ep$ (BD 1080p) [Echo-Subs]",
    mkv_title_naming=R"$show$ - E$ep$ - $title$",
    out_dir="muxed",
    clean_work_dirs=False
)

video_file = GlobSearch(f"PriPara - {setup.episode}*.mkv", dir="./")
premux = Premux(video_file, subtitles=None, keep_attachments=False, mkvmerge_args=["--no-global-tags", "--no-chapters"])
subtitle = SubFile(GlobSearch("*_dialogue.ass", allow_multiple=True, dir=f"./{setup.episode}/"))
chapters = Chapters.from_sub(subtitle, use_actor_field=True)
subtitle.merge(GlobSearch("*_insert1.ass", allow_multiple=True, dir=f"./{setup.episode}/"))
subtitle.merge(GlobSearch("*_insert2.ass", allow_multiple=True, dir=f"./{setup.episode}/"))
subtitle.merge(GlobSearch("*_insert3.ass", allow_multiple=True, dir=f"./{setup.episode}/"))
subtitle.merge(GlobSearch("*_insert4.ass", allow_multiple=True, dir=f"./{setup.episode}/"))
subtitle.merge(GlobSearch("*_insert5.ass", allow_multiple=True, dir=f"./{setup.episode}/"))
subtitle.clean_garbage().clean_extradata().set_headers(
    (ASSHeader.PlayResX, 1920),
    (ASSHeader.PlayResY, 1080),
    (ASSHeader.LayoutResX, 1920),
    (ASSHeader.LayoutResY, 1080),
    (ASSHeader.ScaledBorderAndShadow, True),
    (ASSHeader.WrapStyle, 2),
    ("Title", "Echo-subs")
)
fonts = subtitle.collect_fonts()
mux(
    premux,
    subtitle.to_track("English", "en"),
    *fonts,
    chapters,
    tmdb=TmdbConfig(67627)
)