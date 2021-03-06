#!/usr/bin/env python
# encoding: utf-8

import os
import sys

import django
from modularodm import Q
from modularodm.exceptions import ModularOdmException
django.setup()

from osf.models import Conference, OSFUser as User

from website import settings
from website.app import init_app
from datetime import datetime


def main():
    init_app(set_backends=True, routes=False)
    dev = 'dev' in sys.argv
    populate_conferences(dev=dev)


MEETING_DATA = {
    'spsp2014': {
        'name': 'Society for Personality and Social Psychology 2014',
        'info_url': None,
        'logo_url': None,
        'location': 'Austin, TX',
        'start_date': 'Feb 13 2014',
        'end_date': 'Feb 15 2014',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'asb2014': {
        'name': 'Association of Southeastern Biologists 2014',
        'info_url': 'http://www.sebiologists.org/meetings/talks_posters.html',
        'logo_url': None,
        'location': 'Spartanburg, SC',
        'start_date': 'Apr 2 2014',
        'end_date': 'Apr 4 2014',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'aps2014': {
        'name': 'Association for Psychological Science 2014',
        'info_url': 'https://cos.io/aps/',
        'logo_url': '/static/img/2014_Convention_banner-with-APS_700px.jpg',
        'location': 'San Franscisco, CA',
        'start_date': 'May 22 2014',
        'end_date': 'May 25 2014',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'annopeer2014': {
        'name': '#annopeer',
        'info_url': None,
        'logo_url': None,
        'location': None,
        'start_date': None,
        'end_date': None,
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'cpa2014': {
        'name': 'Canadian Psychological Association 2014',
        'info_url': None,
        'logo_url': None,
        'location': 'Vancouver, BC',
        'start_date': 'Jun 05 2014',
        'end_date': 'Jun 07 2014',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'filaments2014': {
        'name': 'National Radio Astronomy Observatory Filaments 2014',
        'info_url': None,
        'logo_url': 'https://science.nrao.edu/science/meetings/2014/'
                    'filamentary-structure/images/filaments2014_660x178.png',
        'location': 'Charlottesville, VA',
        'start_date': 'Oct 10 2014',
        'end_date': 'Oct 11 2014',
        'active': False,
        'admins': [
            'lvonschi@nrao.edu',
            # 'Dkim@nrao.edu',
        ],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'bitss2014': {
        'name': 'Berkeley Initiative for Transparency in the Social Sciences Research Transparency Forum 2014',
        'info_url': None,
        'logo_url': os.path.join(
            settings.STATIC_URL_PATH,
            'img',
            'conferences',
            'bitss.jpg',
        ),
        'location': 'Berkeley, CA',
        'start_date': 'Dec 11 2014',
        'end_date': 'Dec 12 2014',
        'active': False,
        'admins': [
            'gkroll@berkeley.edu',
            'awais@berkeley.edu',
        ],
        'public_projects': True,
        'poster': False,
        'talk': True,
        'is_meeting': True
    },
    'spsp2015': {
        'name': 'Society for Personality and Social Psychology 2015',
        'info_url': None,
        'logo_url': None,
        'location': 'Long Beach, CA',
        'start_date': 'Feb 26 2015',
        'end_date': 'Feb 28 2015',
        'active': False,
        'admins': [
            'meetings@spsp.org',
        ],
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'aps2015': {
        'name': 'Association for Psychological Science 2015',
        'info_url': None,
        'logo_url': 'http://www.psychologicalscience.org/images/APS_2015_Banner_990x157.jpg',
        'location': 'New York, NY',
        'start_date': 'May 21 2015',
        'end_date': 'May 24 2015',
        'admins': [],
        'active': False,
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'icps2015': {
        'name': 'International Convention of Psychological Science 2015',
        'info_url': None,
        'logo_url': 'http://icps.psychologicalscience.org/wp-content/themes/deepblue/images/ICPS_Website-header_990px.jpg',
        'location': 'Amsterdam, The Netherlands',
        'start_date': 'Mar 12 2015',
        'end_date': 'Mar 14 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'mpa2015': {
        'name': 'Midwestern Psychological Association 2015',
        'info_url': None,
        'logo_url': 'http://www.midwesternpsych.org/resources/Pictures/MPA%20logo.jpg',
        'location': 'Chicago, IL',
        'start_date': 'Apr 30 2015',
        'end_date': 'May 02 2015',
        'active': False,
        'admins': [
            'mpa@kent.edu',
        ],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'NCCC2015': {
        'name': 'North Carolina Cognition Conference 2015',
        'info_url': None,
        'logo_url': None,
        'location': 'Elon, NC',
        'start_date': 'Feb 21 2015',
        'end_date': 'Feb 21 2015',
        'active': False,
        'admins': [
            'aoverman@elon.edu',
        ],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'VPRSF2015': {
        'name': 'Virginia Piedmont Regional Science Fair 2015',
        'info_url': None,
        'logo_url': 'http://vprsf.org/wp-content/themes/VPRSF/images/logo.png',
        'location': 'Charlottesville, VA',
        'start_date': 'Mar 17 2015',
        'end_date': 'Mar 17 2015',
        'active': False,
        'admins': [
            'director@vprsf.org',
        ],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'APRS2015': {
        'name': 'UVA Annual Postdoctoral Research Symposium 2015',
        'info_url': None,
        'logo_url': 'http://s1.postimg.org/50qj9u6i7/GPA_Logo.jpg',
        'location': 'Charlottesville, VA',
        'start_date': None,
        'end_date': None,
        'active': False,
        'admins': [
            'mhurst@virginia.edu',
        ],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'ASB2015': {
        'name': 'Association of Southeastern Biologists 2015',
        'info_url': None,
        'logo_url': 'http://www.sebiologists.org/wp/wp-content/uploads/2014/09/banner_image_Large.png',
        'location': 'Chattanooga, TN',
        'start_date': 'Apr 01 2015',
        'end_date': 'Apr 04 2015',
        'active': False,
        'admins': [
            'amorris.mtsu@gmail.com',
        ],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'TeaP2015': {
        'name': 'Tagung experimentell arbeitender Psychologen 2015',
        'info_url': None,
        'logo_url': None,
        'location': 'Hildesheim, Germany',
        'start_date': 'Mar 08 2015',
        'end_date': 'Mar 11 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'VSSEF2015': {
        'name': 'Virginia State Science and Engineering Fair 2015',
        'info_url': 'http://www.vmi.edu/conferences/vssef/vssef_home/',
        'logo_url': 'http://www.vmi.edu/uploadedImages/Images/Headers/vssef4.jpg',
        'location': 'Lexington, VA',
        'start_date': 'Mar 27 2015',
        'end_date': 'Mar 28 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'RMPA2015': {
        'name': 'Rocky Mountain Psychological Association 2015',
        'info_url': 'http://www.rockymountainpsych.org/uploads/7/4/2/6/7426961/85th_annual_rmpa_conference_program_hr.pdf',
        'logo_url': 'http://www.rockymountainpsych.org/uploads/7/4/2/6/7426961/header_images/1397234084.jpg',
        'location': 'Boise, Idaho',
        'start_date': 'Apr 09 2015',
        'end_date': 'Apr 11 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'ARP2015': {
        'name': 'Association for Research in Personality 2015',
        'info_url': 'http://www.personality-arp.org/conference/',
        'logo_url': 'http://www.personality-arp.org/wp-content/uploads/conference/st-louis-arp.jpg',
        'location': 'St. Louis, MO',
        'start_date': 'Jun 11 2015',
        'end_date': 'Jun 13 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'SEP2015': {
        'name': 'Society of Experimental Psychologists Meeting 2015',
        'info_url': 'http://faculty.virginia.edu/Society_of_Experimental_Psychologists/',
        'logo_url': 'http://www.sepsych.org/nav/images/SEP-header.gif',
        'location': 'Charlottesville, VA',
        'start_date': 'Apr 17 2015',
        'end_date': 'Apr 18 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'Reid2015': {
        'name': 'L. Starling Reid Undergraduate Psychology Conference 2015',
        'info_url': 'http://avillage.web.virginia.edu/Psych/Conference',
        'location': 'Charlottesville, VA',
        'start_date': 'Apr 17 2015',
        'end_date': 'Apr 17 2015',
        'logo_url': None,
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'NEEPS2015': {
        'name': 'Northeastern Evolutionary Psychology Conference 2015',
        'info_url': 'http://neeps2015.weebly.com/',
        'location': 'Boston, MA',
        'start_date': 'Apr 09 2015',
        'end_date': 'Apr 11 2015',
        'logo_url': None,
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'VaACS2015': {
        'name': 'Virginia Section American Chemical Society Student Poster Session 2015',
        'info_url': 'http://virginia.sites.acs.org/',
        'logo_url': 'http://virginia.sites.acs.org/Bulletin/15/UVA.jpg',
        'location': 'Charlottesville, VA',
        'start_date': 'Apr 17 2015',
        'end_date': 'Apr 17 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'MADSSCi2015': {
        'name': 'Mid-Atlantic Directors and Staff of Scientific Cores & Southeastern Association of Shared Services 2015',
        'info_url': 'http://madssci.abrf.org',
        'logo_url': 'http://s24.postimg.org/qtc3baefp/2015madssci_seasr.png',
        'location': 'Charlottesville, VA',
        'start_date': 'Jun 03 2015',
        'end_date': 'Jun 5 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'NRAO2015': {
        'name': 'National Radio Astronomy Observatory Accretion 2015',
        'info_url': 'https://science.nrao.edu/science/meetings/2015/accretion2015/posters',
        'location': 'Charlottesville, VA',
        'start_date': 'Oct 09 2015',
        'end_date': 'Oct 10 2015',
        'logo_url': None,
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'ARCS2015': {
        'name': 'Advancing Research Communication and Scholarship 2015',
        'info_url': 'http://commons.pacificu.edu/arcs/',
        'logo_url': 'http://commons.pacificu.edu/assets/md5images/4dfd167454e9f4745360a9550e189323.png',
        'location': 'Philadelphia, PA',
        'start_date': 'Apr 26 2015',
        'end_date': 'Apr 28 2015',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'singlecasedesigns2015': {
        'name': 'Single Case Designs in Clinical Psychology: Uniting Research and Practice',
        'info_url': 'https://www.royalholloway.ac.uk/psychology/events/eventsarticles/singlecasedesignsinclinicalpsychologyunitingresearchandpractice.aspx',
        'logo_url': None,
        'location': 'London, UK',
        'start_date': 'Apr 17 2015',
        'end_date': 'Apr 17 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'OSFM2015': {
        'name': 'OSF for Meetings 2015',
        'info_url': None,
        'logo_url': None,
        'location': 'Charlottesville, VA',
        'start_date': None,
        'end_date': None,
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'JSSP2015': {
        'name': 'Japanese Society of Social Psychology 2015',
        'info_url': 'http://www.socialpsychology.jp/conf2015/index.html',
        'logo_url': None,
        'location': 'Tokyo, Japan',
        'start_date': 'Oct 31 2015',
        'end_date': 'Nov 01 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    '4S2015': {
        'name': 'Society for Social Studies of Science 2015',
        'info_url': 'http://www.4sonline.org/meeting',
        'logo_url': 'http://www.4sonline.org/ee/denver-skyline.jpg',
        'location': 'Denver, CO',
        'start_date': 'Nov 11 2015',
        'end_date': 'Nov 14 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'IARR2016': {
        'name': 'International Association for Relationship Research 2016',
        'info_url': 'http://iarr.psych.utoronto.ca/',
        'logo_url': None,
        'location': 'Toronto, Canada',
        'start_date': 'Jul 20 2016',
        'end_date': 'Jul 24 2016',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'IA2015': {
        'name': 'Inclusive Astronomy 2015',
        'info_url': 'https://vanderbilt.irisregistration.com/Home/Site?code=InclusiveAstronomy2015',
        'logo_url': 'https://vanderbilt.blob.core.windows.net/images/Inclusive%20Astronomy.jpg',
        'location': 'Nashville, TN',
        'start_date': 'Jun 17 2015',
        'end_date': 'Jun 19 2015',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'R2RC': {
        'name': 'Right to Research Coalition',
        'info_url': None,
        'logo_url': None,
        'location': None,
        'start_date': None,
        'end_date': None,
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'OpenCon2015': {
        'name': 'OpenCon2015',
        'info_url': 'http://opencon2015.org/',
        'logo_url': 'http://s8.postimg.org/w9b30pxyd/Open_Con2015_new_logo.png',
        'location': 'Brussels, Belgium',
        'start_date': 'Nov 14 2015',
        'end_date': 'Nov 16 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'ESIP2015': {
        'name': 'Earth Science Information Partners 2015',
        'info_url': 'http://esipfed.org/',
        'logo_url': 'http://s30.postimg.org/m2uz2g4pt/ESIP.png',
        'location': None,
        'start_date': None,
        'end_date': None,
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'SPSP2016': {
        'name': 'Society for Personality and Social Psychology 2016 ',
        'info_url': 'http://meeting.spsp.org',
        'logo_url': None,
        'location': 'San Diego, CA',
        'start_date': 'Jan 28 2016',
        'end_date': 'Jan 30 2016',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'NACIII': {
        'name': '2015 National Astronomy Consortium (NAC) III Workshop',
        'info_url': 'https://info.nrao.edu/do/odi/meetings/2015/nac111/',
        'logo_url': None,
        'location': 'Washington, DC',
        'start_date': 'Aug 29 2015',
        'end_date': 'Aug 30 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'CDS2015': {
        'name': 'Cognitive Development Society 2015',
        'info_url': 'http://meetings.cogdevsoc.org/',
        'logo_url': None,
        'location': 'Columbus, OH',
        'start_date': 'Oct 09 2015',
        'end_date': 'Oct 10 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'SEASR2016': {
        'name': 'Southeastern Association of Shared Resources 2016',
        'info_url': 'http://seasr.abrf.org',
        'logo_url': None,
        'location': 'Atlanta, GA',
        'start_date': 'Jun 22 2016',
        'end_date': 'Jun 24 2016',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'Accretion2015': {
        'name': 'Observational Evidence of Gas Accretion onto Galaxies?',
        'info_url': 'https://science.nrao.edu/science/meetings/2015/accretion2015',
        'logo_url': None,
        'location':'Charlottesville, VA',
        'start_date':'Oct 09 2015',
        'end_date':'Oct 10 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    '2020Futures': {
        'name': 'U.S. Radio/Millimeter/Submillimeter Science Futures in the 2020s',
        'info_url': 'https://science.nrao.edu/science/meetings/2015/2020futures/home',
        'logo_url': None,
        'location':'Chicago, IL',
        'start_date':'Dec 15 2015',
        'end_date':'Dec 17 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'RMPA2016': {
        'name': 'Rocky Mountain Psychological Association 2016',
        'info_url': 'http://www.rockymountainpsych.org/convention-info.html',
        'logo_url': 'http://www.rockymountainpsych.org/uploads/7/4/2/6/7426961/header_images/1397234084.jpg',
        'location':'Denver, CO',
        'start_date':'Apr 14 2016',
        'end_date':'Apr 16 2016',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'CNI2015': {
        'name': 'Coalition for Networked Information (CNI) Fall Membership Meeting 2015',
        'info_url': 'https://wp.me/P1LncT-64s',
        'logo_url': None,
        'location':'Washington, DC',
        'start_date':'Dec 14 2015',
        'end_date':'Dec 16 2015',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': False,
        'talk': True,
        'is_meeting': True
    },
    'SWPA2016': {
        'name': 'Southwestern Psychological Association Convention 2016',
        'info_url': 'https://www.swpsych.org/conv_dates.php',
        'logo_url': 'http://s28.postimg.org/xbwyqqvx9/SWPAlogo4.jpg',
        'location':'Dallas, TX',
        'start_date':'Apr 08 2016',
        'end_date':'Apr 10 2016',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'ESIP2016W': {
        'name': 'Earth Science Information Partners Winter Meeting 2016',
        'info_url': 'http://commons.esipfed.org/2016WinterMeeting',
        'logo_url': 'http://s30.postimg.org/m2uz2g4pt/ESIP.png',
        'location':'Washington, DC',
        'start_date':'Jan 06 2016',
        'end_date':'Jan 08 2016',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'MiamiBrainhack15': {
        'name': 'University of Miami Brainhack 2015',
        'info_url': 'http://brainhack.org/americas/',
        'logo_url': None,
        'location': None,
        'start_date': 'Oct 23 2015',
        'end_date': 'Oct 25 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'PsiChiRepository': {
        'name': 'Psi Chi',
        'location': None,
        'start_date': None,
        'end_date': None,
        'info_url': 'http://www.psichi.org/?ResearchAdvisory#.VmBpeOMrI1g',
        'logo_url': 'http://s11.postimg.org/4g2451vcz/Psi_Chi_Logo.png',
        'active': True,
        'admins': [
            'research.director@psichi.org',
        ],
        'field_names': {
            'submission1': 'measures',
            'submission2': 'materials',
            'submission1_plural': 'measures/scales',
            'submission2_plural': 'study materials',
            'meeting_title_type': 'Repository',
            'add_submission': 'materials',
            'mail_subject': 'Title',
            'mail_message_body': 'Measure or material short description',
            'mail_attachment': 'Your measure/scale or material file(s)'
        },
        'is_meeting': False
    },
    'GI2015': {
        'name': 'Genome Informatics 2015',
        'info_url': 'https://meetings.cshl.edu/meetings.aspx?meet=info&year=15',
        'logo_url': None,
        'location':'Cold Spring Harbor, NY' ,
        'start_date': 'Oct 28 2015',
        'end_date': 'Oct 31 2015',
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'MADSSCi2016': {
        'name': 'Mid-Atlantic Directors and Staff of Scientific Cores & Southeastern Association of Shared Services 2016',
        'info_url': 'http://madssci.abrf.org',
        'logo_url': 'http://madssci.abrf.org/sites/default/files/madssci-logo-bk.png',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'SMM2015': {
        'name': 'The Society for Marine Mammalogy',
        'info_url': 'https://www.marinemammalscience.org/conference/',
        'logo_url': None,
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'TESS': {
        'name': 'Time-sharing Experiments for the Social Sciences',
        'info_url': 'http://www.tessexperiments.org',
        'logo_url': None,
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': False,
        'talk': True,
        'field_names': {
            'submission1': 'poster',
            'submission2': 'study',
            'submission1_plural': 'posters',
            'submission2_plural': 'studies',
            'meeting_title_type': 'Studies',
            'add_submission': 'studies',
        },
        'is_meeting': False
    },
    'ASCERM2016': {
        'name': 'ASCE Rocky Mountain Student Conference 2016',
        'info_url': 'http://luninuxos.com/asce/',
        'logo_url': 'http://s2.postimg.org/eaduh2ovt/2016_ASCE_Rocky_Mtn_banner.png',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': False,
        'talk': True,
        'is_meeting': True
    },
    'ARCA2016': {
        'name': '5th Applied Research Conference in Africa',
        'info_url': 'http://www.arcaconference.org/',
        'logo_url': 'http://www.arcaconference.org/images/ARCA_LOGO_NEW.JPG',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': False,
        'talk': True,
        'is_meeting': True
    },
    'CURCONF2016': {
        'name': 'CUR Biennial Conference 2016',
        'info_url': 'http://www.cur.org/conferences_and_events/biennial2016/',
        'logo_url': 'http://s11.postimg.org/v8feuna4y/Conference_logo_eps.jpg',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'CATALISE2016': {
        'name': 'Criteria and Terminology Applied to Language Impairments: Synthesising the Evidence (CATALISE) 2016',
        'info_url': None,
        'logo_url': None,
        'active': False,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'Emergy2016': {
        'name': '9th Biennial Emergy Research Conference',
        'info_url': 'http://www.cep.ees.ufl.edu/emergy/conferences/ERC09_2016/index.shtml',
        'logo_url': 'http://s12.postimg.org/uf9ioqmct/emergy.jpg',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'aps2016': {
        'name': 'Association for Psychological Science 2016',
        'info_url': 'http://www.psychologicalscience.org/convention',
        'logo_url': 'http://www.psychologicalscience.org/redesign/wp-content/uploads/2015/03/APS_2016_Banner_990x157.jpg',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'jssp2016': {
        'name': 'Japanese Society of Social Psychology 2016',
        'info_url': 'http://www.socialpsychology.jp/conf2016/',
        'logo_url': None,
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'sepech2016': {
        'name': 'XI SEPECH - Research Seminar in Human Sciences (Seminário de Pesquisa em Ciências Humanas)',
        'info_url': 'http://www.uel.br/eventos/sepech/sepech2016/',
        'logo_url': None,
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'etmaal2016': {
        'name': 'Etmaal van de Communicatiewetenschap 2016 - Media Psychology',
        'info_url': 'https://etmaal2016.wordpress.com',
        'logo_url': None,
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'WSAN2016': {
        'name': 'WSAN2016 Erasmus University Rotterdam',
        'info_url': 'http://www.humane.eu/wsan/',
        'logo_url': None,
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'ContainerStrategies': {
        'name': 'Container Strategies for Data & Software Preservation',
        'info_url': 'https://daspos.crc.nd.edu/index.php/workshops/container-strategies-for-data-software-preservation-that-promote-open-science',
        'logo_url': 'http://s17.postimg.org/8nl1v5mxb/Screen_Shot_2016_03_02_at_9_05_24_PM.png',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'is_meeting': True
    },
    'CNI2016': {
        'name': 'Coalition for Networked Information (CNI) Spring Membership Meeting 2016',
        'info_url': 'https://wp.me/P1LncT-6fd',
        'logo_url': None,
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': False,
        'talk': True,
        'is_meeting': True
    },
    'XGAL2016': {
        'name': 'Molecular Gas in Galactic Environments 2016',
        'info_url': 'https://science.nrao.edu/science/meetings/2016/molecular-gas-in-galactic-environments/home',
        'logo_url': None,
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'DLF2016': {
        'name': 'Digital Library Federation 2016 DLF Forum',
        'info_url': 'https://www.diglib.org/forums/2016forum/',
        'logo_url': 'https://www.diglib.org/wp-content/themes/construct/lib/scripts/timthumb/thumb.php?src=https://www.diglib.org/wp-content/uploads/2016/02/DLF-Forum-2016-Slider-Website-1.png&w=580&h=252&zc=1&q=100',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'start_date': 'Nov 7 2016',
        'end_date': 'Nov 9 2016',
        'locztion': 'Milwaukee, Wisconsin',
        'is_meeting': True
    },
    'ESCAN2016': {
        'name': 'European Society for Cognitive and Affective Neuroscience (ESCAN) 2016',
        'info_url': 'http://congressos.abreu.pt/escan2016/',
        'logo_url': 'http://congressos.abreu.pt/escan2016/images/escan-logo.png',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'Reid2016': {
        'name': 'L. Starling Reid Undergraduate Psychology Conference 2016',
        'info_url': 'http://cacsprd.web.virginia.edu/Psych/Conference',
        'logo_url': None,
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'CNS2016': {
        'name': 'The Cognitive Neuroscience Society (CNS) 2016',
        'info_url': 'http://www.cogneurosociety.org/annual-meeting/',
        'logo_url': None,
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'HEPA2016': {
        'name': 'HEPA Europe Annual Meeting 2016',
        'info_url': 'http://www.hepaeurope2016.eu/',
        'logo_url': None,
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
    'OGH': {
        'name': 'Open Global Health',
        'info_url': None,
        'logo_url': 'http://s33.postimg.org/7tjjpvg4f/Drawing.png',
        'active': True,
        'admins': [],
        'public_projects': True,
        'poster': True,
        'talk': True,
        'is_meeting': True
    },
}


def populate_conferences(dev=False):
    if dev:
        Conference.remove()
    date_format = '%b %d %Y'
    for meeting, attrs in MEETING_DATA.iteritems():
        meeting = meeting.strip()
        admin_emails = attrs.pop('admins', [])
        admin_objs = []
        if not dev:
            for email in admin_emails:
                try:
                    user = User.find_one(Q('username', 'iexact', email))
                    admin_objs.append(user)
                except ModularOdmException:
                    raise RuntimeError('Username {0!r} is not registered.'.format(email))

        # Convert string into datetime object
        try:
            attrs['end_date'] = datetime.strptime(attrs.get('end_date'), date_format)
            attrs['start_date'] = datetime.strptime(attrs.get('start_date'), date_format)
        except TypeError:
            print '** Meeting {} does not have a start or end date. **'.format(meeting)
        custom_fields = attrs.pop('field_names', {})

        conf = Conference(
            endpoint=meeting, admins=admin_objs, **attrs
        )
        conf.field_names.update(custom_fields)
        try:
            conf.save()
        except ModularOdmException:
            conf = Conference.find_one(Q('endpoint', 'eq', meeting))
            for key, value in attrs.items():
                if isinstance(value, dict):
                    current = getattr(conf, key)
                    current.update(value)
                    setattr(conf, key, current)
                else:
                    setattr(conf, key, value)
            conf.admins = admin_objs
            changed_fields = conf.save()
            if changed_fields:
                print('Updated {}: {}'.format(meeting, changed_fields))
        else:
            print('Added new Conference: {}'.format(meeting))


if __name__ == '__main__':
    main()
