# Public candidate-source catalog only. No benchmark selection or evaluation schedule.
# Source archives are fixed-output fetches; no upstream build scripts are executed.
{ fetchzip }:
let
  make = { id, repository, revision, package, declaredEngineVersion, historicalTier, hash }:
    {
      inherit id repository revision package declaredEngineVersion historicalTier;
      sourceNarHash = hash;
      sourceRoot = "src/${package}";
      licensePath = "LICENSE";
      license = "AGPL-3.0";
      licenseSha256 = "76a97c878c9c7a8321bb395c2b44d3fe2f8d81314d219b20138ed0e2dddd5182";
      src = fetchzip {
        name = "bc23-${id}-source";
        url = "https://github.com/${repository}/archive/${revision}.tar.gz";
        inherit hash;
      };
    };
in {
  lectureplayer = make {
    id = "lectureplayer";
    hash = "sha256-VgVZukWaQ56FlNIKf2yhIiunbm/0p0ISnc963a6XHO8=";
    repository = "battlecode/battlecode23-lectureplayer";
    revision = "57063ad07b2311c21c99ba7be100a55fcdb3de6b";
    package = "lectureplayer";
    declaredEngineVersion = "2.0.1";
    historicalTier = "tutorial";
  };
  beaverbois = make {
    id = "beaverbois";
    hash = "sha256-/gRZ+d4O06AvXA3k4E04G8jr3VdD+tpKhNppuETAHIs=";
    repository = "beaverbois/battlecode23";
    revision = "4892382943da5a8527906467739a64db51ccc50d";
    package = "USQualifiers";
    declaredEngineVersion = "3.0.5";
    historicalTier = "non-finalist-field";
  };
  no_thoughts = make {
    id = "no-thoughts";
    hash = "sha256-2n2yjnpvMZrnt4UNyfwik001v5YxG7yPrrWTl7ck2Y8=";
    repository = "reeceyang/battlecode-2023";
    revision = "0a9a855ea15780f692dc994a390e39041a184597";
    package = "v5anaconda";
    declaredEngineVersion = "3.0.13";
    historicalTier = "newbie-runner-up";
  };
  gone_fishin = make {
    id = "gone-fishin";
    hash = "sha256-/BhvNZnaUqGFMRZcBqDT3Ia55FHujBjHxib5CqDhRaU=";
    repository = "carlguo866/battlecode23-gonefishin";
    revision = "1c3ff39bca59e302c6c1092025e413bd0a102ab9";
    package = "submit26_final";
    declaredEngineVersion = "3.0.13";
    historicalTier = "finalist-runner-up";
  };
  four_musketeers = make {
    id = "four-musketeers";
    hash = "sha256-USWoQxph1sdmpaCeu0uUz/qv/2KoPDcV7Nfre4sRwgs=";
    repository = "maxwelljones14/BattleCode2023";
    revision = "074963dacf1c597518655de4c7542c36de6bc554";
    package = "MPWorking";
    declaredEngineVersion = "3.0.13";
    historicalTier = "finalist-third";
  };
  dont_at_me = make {
    id = "dont-at-me";
    hash = "sha256-sc4D+D+9XU4I89kkGR5EtMCXwmqIaNmSFJ/RJY6RFwo=";
    repository = "georgezhang02/battlecode23";
    revision = "83f81b5568772ecb4f77af462f512dae7aaa4968";
    package = "FB_ZZZ";
    declaredEngineVersion = "3.0.13";
    historicalTier = "finalist-official-history-seventh";
  };
}
