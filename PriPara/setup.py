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
# dialogue = GlobSearch("*dialogue*.ass", dir=f"./{setup.episode}/")
subtitle = SubFile(GlobSearch("*_dialogue.ass", allow_multiple=True, dir=f"./{setup.episode}/"))
chapters = Chapters.from_sub(subtitle, use_actor_field=True)
subtitle.merge(GlobSearch("*_insert*.ass", allow_multiple=True, dir=f"./{setup.episode}/"))
# songs = GlobSearch("*insert*.ass",allow_multiple=True, dir=f"./{setup.episode}/").paths

fonts = subtitle.collect_fonts()
mux(
    premux,
    subtitle.to_track("English", "en"),
    *fonts, 
    chapters,
    tmdb=TmdbConfig(67627)
)