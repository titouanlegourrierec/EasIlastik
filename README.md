<!----------------------------------------------------------------------->
<a name="readme-top"></a>
<!----------------------------------------------------------------------->

<table width="100%" style="border: none;">
  <tr>
    <td align="left" style="border: none;"><b>LE GOURRIEREC Titouan</b></td>
    <td align="left" style="border: none;"></td>
    <td align="right" style="border: none;">
      <a href="https://www.linkedin.com/in/titouanlegourrierec"><img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
      <a href="mailto:titouanlegourrieræec@icloud.com"><img src="https://img.shields.io/badge/email-%23339933.svg?style=for-the-badge&logo=mail.ru&logoColor=white" alt="Mail"></a>
    </td>
  </tr>
</table>

<!----------------------------------------------------------------------->
<!----------------------------------------------------------------------->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">EasIlastik </h3>

  <p align="center">
    A package to facilitate the use of image segmentation model trained on Ilastik in Python
    <br />
    <a href="https://github.com/titouanlegourrierec/EasIlastik/wiki"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://github.com/titouanlegourrierec/EasIlastik/issues">Report a bug · Request Feature</a>
  </p>
  <p align="center">
    <a href="https://pypi.org/project/EasIlastik/">
      <img src="https://img.shields.io/pypi/v/EasIlastik.svg" alt="PyPI Version">
    </a>
    </a>
        <a href="https://pepy.tech/projects/easilastik">
      <img src="https://static.pepy.tech/badge/easilastik" alt="Downloads">
    </a>
    <a href="https://github.com/psf/black">
      <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style: Black">
    </a>
    <a href="https://github.com/titouanlegourrierec/EasIlastik/blob/main/LICENSE">
      <img src="https://img.shields.io/github/license/titouanlegourrierec/EasIlastik.svg" alt="License">
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project 📖</a>
      <ul>
        <li><a href="#built-with">Built With 🛠️</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!----------------------------------------------------------------------->
<!----------------------------------------------------------------------->

## About The Project

<p align="center">
  <img src="https://raw.githubusercontent.com/titouanlegourrierec/EasIlastik/main/assets/img.png" width="100%">
</p>

This package provides seamless integration of pre-trained image segmentation models from Ilastik into Python workflows, empowering users with efficient and intuitive image segmentation capabilities for diverse applications.

<!----------------------------------------------------------------------->
<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!----------------------------------------------------------------------->


### Built With
* [![Python][Python-badge]][Python-url]
* [![OpenCV][OpenCV-badge]][OpenCV-url]
* ![Shell Script][ShellScript-badge]


<!----------------------------------------------------------------------->
<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!----------------------------------------------------------------------->

## Getting Started
### Prerequisites 

* **Ilastik software**: To train your own model for image segmentation, please download the Ilastik software tailored to your computer's operating system from: https://www.ilastik.org/download.

### Train a model

* To train your own model on Ilastik and properly adjust the different parameters, please refer to [this documentation](https://github.com/titouanlegourrierec/EasIlastik/wiki/Train-a-model-on-Ilastik).




<!----------------------------------------------------------------------->
<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!----------------------------------------------------------------------->


## Usage

For usage examples of this package, please refer to the [Example Notebook](https://github.com/titouanlegourrierec/EasIlastik/blob/1be43ebb76bccec6917e05367fbb7e48b184efdc/Examples/example-notebook.ipynb).

### Process a single image
```python
EasIlastik.run_ilastik(input_path = "path/to/your/image.jpg", # The path of the image to process
                       model_path = "path/to/your/model.ilp",
                       result_base_path = "path/to/your/output/folder/",
                       export_source = "Simple Segmentation",
                       output_format = "png")
```
<p align="center">
  <img src="https://raw.githubusercontent.com/titouanlegourrierec/EasIlastik/main/assets/run_ilastik_image.png" alt="run_ilastik_image" width="50%">
</p>

### Process a folder of images
```python
EasIlastik.run_ilastik(input_path = "path/to/input/folder", # The path of the folder to process
                       model_path = "path/to/your/model.ilp",
                       result_base_path = "path/to/your/output/folder/",
                       export_source = "Simple Segmentation",
                       output_format = "png")
```
<p align="center">
  <img src="https://raw.githubusercontent.com/titouanlegourrierec/EasIlastik/main/assets/run_ilastik_folder.png" alt="run_ilastik_folder" width="70%">
</p>

### Show probabilities
```python
EasIlastik.run_ilastik(input_path = "path/to/input/image",
                       model_path = "path/to/model.ilp",
                       result_base_path = "path/to/output/folder",
                       export_source="Probabilities", # Probabilities
                       output_format="hdf5") # hdf5 format

output_path = "path/to/output/image.h5"
image = EasIlastik.color_treshold_probabilities(output_path, threshold, below_threshold_color, channel_colors)
```
<p align="center">
  <img src="https://raw.githubusercontent.com/titouanlegourrierec/EasIlastik/main/assets/run_ilastik_show_probabilities.png" alt="run_ilastik_probabilities" width="70%">
</p>

### Run with probabilities
```python
EasIlastik.run_ilastik_probabilities(input_path = "path/to/input/folder",
                                     model_path = "path/to/model.ilp",
                                     result_base_path = "path/to/output/folder",
                                     threshold = 70, # threshold for the probabilities
                                     below_threshold_color = [255, 0, 0], # color for the pixels below the threshold (red)
                                     channel_colors = [[63, 63, 63], [127, 127, 127], ...] # colors for the different channels
                                     )
```
<p align="center">
  <img src="https://raw.githubusercontent.com/titouanlegourrierec/EasIlastik/main/assets/run_ilastik_run_probabilities.png" alt="run_ilastik_probabilities" width="70%">
</p>


<!----------------------------------------------------------------------->
<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!----------------------------------------------------------------------->



<!-- ROADMAP -->
<!-- ## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- CONTRIBUTING -->
<!-- ## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->


## License

Distributed under the GNU License like the Ilastik software. See [`LICENSE`](https://github.com/titouanlegourrierec/EasIlastik/blob/1be43ebb76bccec6917e05367fbb7e48b184efdc/LICENCE) for more information.

<!----------------------------------------------------------------------->
<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!----------------------------------------------------------------------->

## Contact

LE GOURRIEREC Titouan - [titouanlegourrierec@icloud.com](mailto:titouanlegourrierec@icloud.com)

Repository Link: [https://github.com/titouanlegourrierec/EasIlastik](https://github.com/titouanlegourrierec/EasIlastik)  
Pypi Link : [https://pypi.org/project/EasIlastik/](https://pypi.org/project/EasIlastik/)


<!----------------------------------------------------------------------->
<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!----------------------------------------------------------------------->


## Acknowledgments

* [Ilastik Software](https://www.ilastik.org) : An interactive interface to annotate images to segment.

<!----------------------------------------------------------------------->
<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!----------------------------------------------------------------------->



<!-- MARKDOWN LINKS & IMAGES -->


[Python-badge]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org

[OpenCV-badge]: https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white
[OpenCV-url]: https://opencv.org

[ShellScript-badge]: https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white