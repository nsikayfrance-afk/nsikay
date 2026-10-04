from enum import Enum


class VideoQuality(Enum):
    SD = "480p"
    HD = "720p"
    FULL_HD = "1080p"
    FOUR_K = "2160p"
    EIGHT_K = "4320p"


class StreamSource(Enum):
    CAMERA = "camera"
    IP_CAMERA = "ip_camera"
    SATELLITE = "satellite"
    FILE = "file"
    LIVE_EXTERNAL = "live_external"


class VideoProcessing:
    """
    Gestion logique traitement vidéo régie NSIKAY
    """

    def __init__(
        self,
        quality="2160p",
        source="camera"
    ):
        self.quality = quality
        self.source = source


    def configure(self):
        return {
            "quality": self.quality,
            "source": self.source,
            "codec": "H265",
            "format": "4K",
            "live_ready": True
        }



class TextOverlayEngine:
    """
    Moteur d'incrustation texte
    """

    def create_overlay(
        self,
        text,
        animation="fade",
        position="bottom"
    ):
        return {
            "text": text,
            "animation": animation,
            "position": position,
            "enabled": True
        }



class VideoEffectEngine:
    """
    Effets vidéo temps réel
    """

    EFFECTS = [
        "transition",
        "blur",
        "color_filter",
        "zoom",
        "fade",
        "special_effect"
    ]


    def apply(self, effect):
        if effect not in self.EFFECTS:
            return {
                "error": "Effet inconnu"
            }

        return {
            "effect": effect,
            "active": True
        }



class AudioMixer:
    """
    Gestion audio régie
    """

    def mix(
        self,
        volume=100,
        noise_filter=True
    ):
        return {
            "volume": volume,
            "noise_filter": noise_filter,
            "processed": True
        }

