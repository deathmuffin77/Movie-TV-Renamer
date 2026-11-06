from pathlib import Path

def main():
 parentpath=Path(__file__).resolve().parent
 moviepath=parentpath.parent / "3.Movies DONE"
 tvpath=parentpath.parent / "2.TV DONE"
 renamerpath=parentpath.parent / ("1.Renamer")
 if(input('Delete completed movies and tv?\n      "y" or "n"' )=="y"):
    for file in moviepath.iterdir():
        print(file.stem)
        file.unlink()
    for file in tvpath.iterdir():
        print(file.stem)
        file.unlink()
 if(input('Delete contents of 1.Renamer?\n      "y" or "n"' )=="y"):
    for file in renamerpath.iterdir():
        print(file.stem)
        file.unlink()
        
main()
 