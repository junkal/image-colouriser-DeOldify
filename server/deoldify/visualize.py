from fastai.core import *
from fastai.vision import *
from .filters import IFilter, MasterFilter, ColorizerFilter
from .generators import gen_inference_deep, gen_inference_wide
from PIL import Image
import gc
import requests
from io import BytesIO
import base64
import cv2

class ModelImageVisualizer:
    def __init__(self, filter: IFilter, results_dir: str = None):
        self.filter = filter
        self.results_dir = None if results_dir is None else Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def _clean_mem(self):
        torch.cuda.empty_cache()
        # gc.collect()

    def _open_pil_image(self, path: Path) -> Image:
        return PIL.Image.open(path).convert('RGB')

    def _get_image_from_url(self, url: str) -> Image:
        response = requests.get(url, timeout=30, headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'})
        img = PIL.Image.open(BytesIO(response.content)).convert('RGB')
        return img

    def plot_transformed_image_from_url(
        self,
        url: str,
        path: str = 'test_images/image.png',
        results_dir:Path = None,
        figsize: Tuple[int, int] = (20, 20),
        render_factor: int = None,

        display_render_factor: bool = False,
        compare: bool = False,
        post_process: bool = True,
        watermarked: bool = True,
    ) -> Path:
        img = self._get_image_from_url(url)
        img.save(path)
        return self.plot_transformed_image(
            path=path,
            results_dir=results_dir,
            figsize=figsize,
            render_factor=render_factor,
            display_render_factor=display_render_factor,
            compare=compare,
            post_process = post_process,
            watermarked=watermarked,
        )

    def get_transformed_image(
        self,
        path: str,
        results_dir:Path = None,
        figsize: Tuple[int, int] = (20, 20),
        render_factor: int = None,
        display_render_factor: bool = False,
        # compare: bool = False,
        post_process: bool = True
        # watermarked: bool = True
    ) -> Path:
        path = Path(path)
        if results_dir is None:
            results_dir = Path(self.results_dir)

        self._clean_mem()
        orig_image = self._open_pil_image(path)
        filtered_image = self.filter.filter(
            orig_image, orig_image, render_factor=render_factor,post_process=post_process
        )

        result_path = self._save_result_image(path, filtered_image, results_dir=results_dir)
        filtered_image.close()
        return result_path

    def _save_result_image(self, source_path: Path, image: Image, results_dir = None) -> Path:
        if results_dir is None:
            results_dir = Path(self.results_dir)
        result_path = results_dir / source_path.name
        image.save(result_path)
        return result_path


def get_image_colorizer(
    root_folder: Path = Path('./'), render_factor: int = 35, artistic: bool = True
) -> ModelImageVisualizer:
    if artistic:
        return get_artistic_image_colorizer(root_folder=root_folder, render_factor=render_factor)
    else:
        return get_stable_image_colorizer(root_folder=root_folder, render_factor=render_factor)


def get_stable_image_colorizer(
    root_folder: Path = Path('./'),
    weights_name: str = 'ColorizeStable_gen',
    results_dir='result_images',
    render_factor: int = 35
) -> ModelImageVisualizer:
    learn = gen_inference_wide(root_folder=root_folder, weights_name=weights_name)
    filtr = MasterFilter([ColorizerFilter(learn=learn)], render_factor=render_factor)
    vis = ModelImageVisualizer(filtr, results_dir=results_dir)
    return vis


def get_artistic_image_colorizer(
    root_folder: Path = Path('./'),
    weights_name: str = 'ColorizeArtistic_gen',
    results_dir='result_images',
    render_factor: int = 35
) -> ModelImageVisualizer:
    learn = gen_inference_deep(root_folder=root_folder, weights_name=weights_name)
    filtr = MasterFilter([ColorizerFilter(learn=learn)], render_factor=render_factor)
    vis = ModelImageVisualizer(filtr, results_dir=results_dir)
    return vis
