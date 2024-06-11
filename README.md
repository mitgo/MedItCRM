[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

# MedItCRM
This project is an attempt to automate and simplify several routine areas of the IT department of a medical organization. At the moment, only one task has been implemented - assistance in issuing EDS for staff. The plans include the implementation of cartridge accounting (warehouse, transfer, refueling, etc.)
, I hope the project will be constantly updated with new functionality.
I also strongly hope that he will be useful to someone other than me.

![Screen][product-screenshot]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started
You need to install docker!
1. clone repo 

```cd /opt```<br />
```git clone https://github.com/mitgo/MedItCRM.git```

2. Go to the MedItCRM directory

```cd MedItCRM```

3. Create users in your infrastructure:
* an user to connect to your AD in order to get users to access MedItCRM
* an same users in your 1C DB to get info about your staff and in your TM MIS to get info about your medstaff (maybe read only user)
4. Create [.env](./docs/env-template.md) file with needed vars in current directory
**It may be necessary to adjust the query code from 1C due to the fact that the names of tables and fields may vary.**

5. Change permissions to entrypoint.sh

```chmod 755 entrypoint.sh```

6. Run docker compose

```docker compose up -d --build```

7. If it neccesary go to the med_it_crm container and create an superuser

```docker exec -it med_it_crm /bin/bash```
```python ./manage.py create superuser```

8. Go to your browser and open http://yourhost/

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Support
If you have any difficulties or questions about using the package, create
[discussion](https://github.com/mitgo/MedItCRM/issues/new/choose) in this repository

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

- [ ] Add install esign tool for ECP APP
- [ ] Refactor ECP APP
- [ ] Add Cartridge APP
- [ ] Add Staistic APP to collect soe statistics from different Med Apps in company
- [ ] Add FSS APP to provide simple update tool fo FSS progs
- [ ] Add MedicalIron APP

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Dmitriy Scherban

Project Link: [https://github.com/mitgo/MedItCRM](https://github.com/mitgo/MedItCRM)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[forks-shield]: https://img.shields.io/github/forks/mitgo/MedItCRM.svg?style=for-the-badge
[forks-url]: https://github.com/mitgo/MedItCRM/network/members
[stars-shield]: https://img.shields.io/github/stars/mitgo/MedItCRM.svg?style=for-the-badge
[stars-url]: https://github.com/mitgo/MedItCRM/stargazers
[issues-shield]: https://img.shields.io/github/issues/mitgo/MedItCRM.svg?style=for-the-badge
[issues-url]: https://github.com/mitgo/MedItCRM/issues
[license-shield]: https://img.shields.io/github/license/mitgo/MedItCRM.svg?style=for-the-badge
[license-url]: https://github.com/mitgo/MedItCRM/blob/master/LICENSE.txt

[product-screenshot]: /docs/images/screenshot.png