from pathlib import Path

# --- Storage ---
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "storage" / "uploads"
OUTPUT_DIR = BASE_DIR / "storage" / "outputs"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Limits ---
MAX_MEDIA_SECONDS = 25 * 60  # 25 minute cap, applies to both video and audio-only uploads
MAX_UPLOAD_BYTES = 500 * 1024 * 1024  # 500MB safety ceiling on file size
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm", ".avi"}
ALLOWED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".wma", ".opus"}
ALLOWED_MEDIA_EXTENSIONS = ALLOWED_VIDEO_EXTENSIONS | ALLOWED_AUDIO_EXTENSIONS

# --- Models ---
WHISPER_MODEL_SIZE = "base"
WHISPER_COMPUTE_TYPE = "int8"
NLLB_MODEL_NAME = "facebook/nllb-200-distilled-600M"

# --- Source languages (what Whisper can recognize being spoken in a video or audio file) ---
# Whisper supports 100 source languages; 97 have a direct NLLB-200 equivalent for
# translation. The 3 without one (Latin, Breton, Hawaiian) are omitted here -
# if Whisper detects one of these, jobs.py falls back to leaving the transcript
# untranslated rather than crashing (see the source_nllb is None branch).
WHISPER_TO_NLLB = {
    "en": "eng_Latn",  # english
    "zh": "zho_Hans",  # chinese
    "de": "deu_Latn",  # german
    "es": "spa_Latn",  # spanish
    "ru": "rus_Cyrl",  # russian
    "ko": "kor_Hang",  # korean
    "fr": "fra_Latn",  # french
    "ja": "jpn_Jpan",  # japanese
    "pt": "por_Latn",  # portuguese
    "tr": "tur_Latn",  # turkish
    "pl": "pol_Latn",  # polish
    "ca": "cat_Latn",  # catalan
    "nl": "nld_Latn",  # dutch
    "ar": "arb_Arab",  # arabic
    "sv": "swe_Latn",  # swedish
    "it": "ita_Latn",  # italian
    "id": "ind_Latn",  # indonesian
    "hi": "hin_Deva",  # hindi
    "fi": "fin_Latn",  # finnish
    "vi": "vie_Latn",  # vietnamese
    "he": "heb_Hebr",  # hebrew
    "uk": "ukr_Cyrl",  # ukrainian
    "el": "ell_Grek",  # greek
    "ms": "zsm_Latn",  # malay
    "cs": "ces_Latn",  # czech
    "ro": "ron_Latn",  # romanian
    "da": "dan_Latn",  # danish
    "hu": "hun_Latn",  # hungarian
    "ta": "tam_Taml",  # tamil
    "no": "nob_Latn",  # norwegian
    "th": "tha_Thai",  # thai
    "ur": "urd_Arab",  # urdu
    "hr": "hrv_Latn",  # croatian
    "bg": "bul_Cyrl",  # bulgarian
    "lt": "lit_Latn",  # lithuanian
    "mi": "mri_Latn",  # maori
    "ml": "mal_Mlym",  # malayalam
    "cy": "cym_Latn",  # welsh
    "sk": "slk_Latn",  # slovak
    "te": "tel_Telu",  # telugu
    "fa": "pes_Arab",  # persian
    "lv": "lvs_Latn",  # latvian
    "bn": "ben_Beng",  # bengali
    "sr": "srp_Cyrl",  # serbian
    "az": "azj_Latn",  # azerbaijani
    "sl": "slv_Latn",  # slovenian
    "kn": "kan_Knda",  # kannada
    "et": "est_Latn",  # estonian
    "mk": "mkd_Cyrl",  # macedonian
    "eu": "eus_Latn",  # basque
    "is": "isl_Latn",  # icelandic
    "hy": "hye_Armn",  # armenian
    "ne": "npi_Deva",  # nepali
    "mn": "khk_Cyrl",  # mongolian
    "bs": "bos_Latn",  # bosnian
    "kk": "kaz_Cyrl",  # kazakh
    "sq": "als_Latn",  # albanian
    "sw": "swh_Latn",  # swahili
    "gl": "glg_Latn",  # galician
    "mr": "mar_Deva",  # marathi
    "pa": "pan_Guru",  # punjabi
    "si": "sin_Sinh",  # sinhala
    "km": "khm_Khmr",  # khmer
    "sn": "sna_Latn",  # shona
    "yo": "yor_Latn",  # yoruba
    "so": "som_Latn",  # somali
    "af": "afr_Latn",  # afrikaans
    "oc": "oci_Latn",  # occitan
    "ka": "kat_Geor",  # georgian
    "be": "bel_Cyrl",  # belarusian
    "tg": "tgk_Cyrl",  # tajik
    "sd": "snd_Arab",  # sindhi
    "gu": "guj_Gujr",  # gujarati
    "am": "amh_Ethi",  # amharic
    "yi": "ydd_Hebr",  # yiddish
    "lo": "lao_Laoo",  # lao
    "uz": "uzn_Latn",  # uzbek
    "fo": "fao_Latn",  # faroese
    "ht": "hat_Latn",  # haitian creole
    "ps": "pbt_Arab",  # pashto
    "tk": "tuk_Latn",  # turkmen
    "nn": "nno_Latn",  # nynorsk
    "mt": "mlt_Latn",  # maltese
    "sa": "san_Deva",  # sanskrit
    "lb": "ltz_Latn",  # luxembourgish
    "my": "mya_Mymr",  # myanmar
    "bo": "bod_Tibt",  # tibetan
    "tl": "tgl_Latn",  # tagalog
    "mg": "plt_Latn",  # malagasy
    "as": "asm_Beng",  # assamese
    "tt": "tat_Cyrl",  # tatar
    "ln": "lin_Latn",  # lingala
    "ha": "hau_Latn",  # hausa
    "ba": "bak_Cyrl",  # bashkir
    "jw": "jav_Latn",  # javanese
    "su": "sun_Latn",  # sundanese
    "yue": "yue_Hant",  # cantonese
}

# --- Target languages (what the user can pick as the subtitle output language) ---
# All 204 FLORES-200 codes NLLB-200 was trained on (includes a few languages with
# more than one script variant, e.g. Chinese Simplified/Traditional).
TARGET_LANGUAGES = {
    "ace_Arab": "Acehnese (Arabic script)",
    "ace_Latn": "Acehnese (Latin script)",
    "acm_Arab": "Mesopotamian Arabic",
    "acq_Arab": "Ta'izzi-Adeni Arabic",
    "aeb_Arab": "Tunisian Arabic",
    "afr_Latn": "Afrikaans",
    "ajp_Arab": "South Levantine Arabic",
    "aka_Latn": "Akan",
    "amh_Ethi": "Amharic",
    "apc_Arab": "North Levantine Arabic",
    "arb_Arab": "Modern Standard Arabic",
    "arb_Latn": "Modern Standard Arabic (Romanized)",
    "ars_Arab": "Najdi Arabic",
    "ary_Arab": "Moroccan Arabic",
    "arz_Arab": "Egyptian Arabic",
    "asm_Beng": "Assamese",
    "ast_Latn": "Asturian",
    "awa_Deva": "Awadhi",
    "ayr_Latn": "Central Aymara",
    "azb_Arab": "South Azerbaijani",
    "azj_Latn": "North Azerbaijani",
    "bak_Cyrl": "Bashkir",
    "bam_Latn": "Bambara",
    "ban_Latn": "Balinese",
    "bel_Cyrl": "Belarusian",
    "bem_Latn": "Bemba",
    "ben_Beng": "Bengali",
    "bho_Deva": "Bhojpuri",
    "bjn_Arab": "Banjar (Arabic script)",
    "bjn_Latn": "Banjar (Latin script)",
    "bod_Tibt": "Standard Tibetan",
    "bos_Latn": "Bosnian",
    "bug_Latn": "Buginese",
    "bul_Cyrl": "Bulgarian",
    "cat_Latn": "Catalan",
    "ceb_Latn": "Cebuano",
    "ces_Latn": "Czech",
    "cjk_Latn": "Chokwe",
    "ckb_Arab": "Central Kurdish",
    "crh_Latn": "Crimean Tatar",
    "cym_Latn": "Welsh",
    "dan_Latn": "Danish",
    "deu_Latn": "German",
    "dik_Latn": "Southwestern Dinka",
    "dyu_Latn": "Dyula",
    "dzo_Tibt": "Dzongkha",
    "ell_Grek": "Greek",
    "eng_Latn": "English",
    "epo_Latn": "Esperanto",
    "est_Latn": "Estonian",
    "eus_Latn": "Basque",
    "ewe_Latn": "Ewe",
    "fao_Latn": "Faroese",
    "fij_Latn": "Fijian",
    "fin_Latn": "Finnish",
    "fon_Latn": "Fon",
    "fra_Latn": "French",
    "fur_Latn": "Friulian",
    "fuv_Latn": "Nigerian Fulfulde",
    "gla_Latn": "Scottish Gaelic",
    "gle_Latn": "Irish",
    "glg_Latn": "Galician",
    "grn_Latn": "Guarani",
    "guj_Gujr": "Gujarati",
    "hat_Latn": "Haitian Creole",
    "hau_Latn": "Hausa",
    "heb_Hebr": "Hebrew",
    "hin_Deva": "Hindi",
    "hne_Deva": "Chhattisgarhi",
    "hrv_Latn": "Croatian",
    "hun_Latn": "Hungarian",
    "hye_Armn": "Armenian",
    "ibo_Latn": "Igbo",
    "ilo_Latn": "Ilocano",
    "ind_Latn": "Indonesian",
    "isl_Latn": "Icelandic",
    "ita_Latn": "Italian",
    "jav_Latn": "Javanese",
    "jpn_Jpan": "Japanese",
    "kab_Latn": "Kabyle",
    "kac_Latn": "Jingpho",
    "kam_Latn": "Kamba",
    "kan_Knda": "Kannada",
    "kas_Arab": "Kashmiri (Arabic script)",
    "kas_Deva": "Kashmiri (Devanagari script)",
    "kat_Geor": "Georgian",
    "knc_Arab": "Central Kanuri (Arabic script)",
    "knc_Latn": "Central Kanuri (Latin script)",
    "kaz_Cyrl": "Kazakh",
    "kbp_Latn": "Kabiye",
    "kea_Latn": "Kabuverdianu",
    "khm_Khmr": "Khmer",
    "kik_Latn": "Kikuyu",
    "kin_Latn": "Kinyarwanda",
    "kir_Cyrl": "Kyrgyz",
    "kmb_Latn": "Kimbundu",
    "kmr_Latn": "Northern Kurdish",
    "kon_Latn": "Kikongo",
    "kor_Hang": "Korean",
    "lao_Laoo": "Lao",
    "lij_Latn": "Ligurian",
    "lim_Latn": "Limburgish",
    "lin_Latn": "Lingala",
    "lit_Latn": "Lithuanian",
    "lmo_Latn": "Lombard",
    "ltg_Latn": "Latgalian",
    "ltz_Latn": "Luxembourgish",
    "lua_Latn": "Luba-Kasai",
    "lug_Latn": "Ganda",
    "luo_Latn": "Luo",
    "lus_Latn": "Mizo",
    "lvs_Latn": "Standard Latvian",
    "mag_Deva": "Magahi",
    "mai_Deva": "Maithili",
    "mal_Mlym": "Malayalam",
    "mar_Deva": "Marathi",
    "min_Arab": "Minangkabau (Arabic script)",
    "min_Latn": "Minangkabau (Latin script)",
    "mkd_Cyrl": "Macedonian",
    "plt_Latn": "Plateau Malagasy",
    "mlt_Latn": "Maltese",
    "mni_Beng": "Meitei (Bengali script)",
    "khk_Cyrl": "Halh Mongolian",
    "mos_Latn": "Mossi",
    "mri_Latn": "Maori",
    "mya_Mymr": "Burmese",
    "nld_Latn": "Dutch",
    "nno_Latn": "Norwegian Nynorsk",
    "nob_Latn": "Norwegian Bokmal",
    "npi_Deva": "Nepali",
    "nso_Latn": "Northern Sotho",
    "nus_Latn": "Nuer",
    "nya_Latn": "Nyanja",
    "oci_Latn": "Occitan",
    "gaz_Latn": "West Central Oromo",
    "ory_Orya": "Odia",
    "pag_Latn": "Pangasinan",
    "pan_Guru": "Eastern Panjabi",
    "pap_Latn": "Papiamento",
    "pes_Arab": "Western Persian",
    "pol_Latn": "Polish",
    "por_Latn": "Portuguese",
    "prs_Arab": "Dari",
    "pbt_Arab": "Southern Pashto",
    "quy_Latn": "Ayacucho Quechua",
    "ron_Latn": "Romanian",
    "run_Latn": "Rundi",
    "rus_Cyrl": "Russian",
    "sag_Latn": "Sango",
    "san_Deva": "Sanskrit",
    "sat_Olck": "Santali",
    "scn_Latn": "Sicilian",
    "shn_Mymr": "Shan",
    "sin_Sinh": "Sinhala",
    "slk_Latn": "Slovak",
    "slv_Latn": "Slovenian",
    "smo_Latn": "Samoan",
    "sna_Latn": "Shona",
    "snd_Arab": "Sindhi",
    "som_Latn": "Somali",
    "sot_Latn": "Southern Sotho",
    "spa_Latn": "Spanish",
    "als_Latn": "Tosk Albanian",
    "srd_Latn": "Sardinian",
    "srp_Cyrl": "Serbian",
    "ssw_Latn": "Swati",
    "sun_Latn": "Sundanese",
    "swe_Latn": "Swedish",
    "swh_Latn": "Swahili",
    "szl_Latn": "Silesian",
    "tam_Taml": "Tamil",
    "tat_Cyrl": "Tatar",
    "tel_Telu": "Telugu",
    "tgk_Cyrl": "Tajik",
    "tgl_Latn": "Tagalog",
    "tha_Thai": "Thai",
    "tir_Ethi": "Tigrinya",
    "taq_Latn": "Tamasheq (Latin script)",
    "taq_Tfng": "Tamasheq (Tifinagh script)",
    "tpi_Latn": "Tok Pisin",
    "tsn_Latn": "Tswana",
    "tso_Latn": "Tsonga",
    "tuk_Latn": "Turkmen",
    "tum_Latn": "Tumbuka",
    "tur_Latn": "Turkish",
    "twi_Latn": "Twi",
    "tzm_Tfng": "Central Atlas Tamazight",
    "uig_Arab": "Uyghur",
    "ukr_Cyrl": "Ukrainian",
    "umb_Latn": "Umbundu",
    "urd_Arab": "Urdu",
    "uzn_Latn": "Northern Uzbek",
    "vec_Latn": "Venetian",
    "vie_Latn": "Vietnamese",
    "war_Latn": "Waray",
    "wol_Latn": "Wolof",
    "xho_Latn": "Xhosa",
    "ydd_Hebr": "Eastern Yiddish",
    "yor_Latn": "Yoruba",
    "yue_Hant": "Yue Chinese",
    "zho_Hans": "Chinese (Simplified)",
    "zho_Hant": "Chinese (Traditional)",
    "zsm_Latn": "Standard Malay",
    "zul_Latn": "Zulu",
}