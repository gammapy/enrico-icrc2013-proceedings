"""Plot example images for the ICRC 2013 proceeding"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as mpl
from astropy.io import fits
from astropy.wcs import WCS
from aplpy import FITSFigure

counts = dict(label='Counts', filename='PKS2155_Test_CountMap.fits')
model = dict(label='Model', filename='PKS2155_Test_ModelMap.fits')
residuals = dict(label='Residuals', filename='PKS2155_Residual_Model_cmap.fits')
images = [counts, model, residuals][::-1]


def set_hgps_style(f):
    """Set HGPS style for a f = aplpy.FITSFigure"""
    #f.set_tick_labels_font(size='small')
    #f.set_axis_labels_font(size='small')
    f.ticks.set_xspacing(2)
    f.ticks.set_yspacing(2)
    f.ticks.set_linewidth(1.5)
    f.tick_labels.set_xformat('dd')
    f.tick_labels.set_yformat('dd')
    f.tick_labels.set_style('colons')
    #f.tick_labels.set_font(size='small')
    f.axis_labels.set_xtext('Right Ascension (deg)')
    f.axis_labels.set_ytext('Declination (deg)')

# Determine image center and width / height
dpi = 2000
header = fits.getheader(images[0]['filename'])
wcs = WCS(header)
header['NAXIS1'] / dpi
header['NAXIS2'] / dpi
lon, lat = header['NAXIS1'] / 2., header['NAXIS2'] / 2.
x_center, y_center = wcs.wcs_pix2world(lon, lat, 0)
radius = header['CDELT2'] * header['NAXIS2'] / 2.
#import IPython; IPython.embed(); 1/0

# Computing the sub-figure sizes is surprisingly hard
figsize=(5, 15)
figure = mpl.figure(figsize=figsize)
axis_ratio = figsize[0] / float(figsize[1])
edge_margin_x = 0.12
edge_margin_y = edge_margin_x * axis_ratio
edge_margin_x_up = 0.01
edge_margin_y_up = edge_margin_x_up * axis_ratio
inner_margin_x = 0.1
inner_margin_y = inner_margin_x * axis_ratio
size_x = (1 - edge_margin_x - edge_margin_x_up)
size_y = (1 - edge_margin_y - edge_margin_y_up - 2 * inner_margin_y) / 3

for ii, image in enumerate(images):
    subplot = [edge_margin_x, edge_margin_y + ii * (size_y + inner_margin_y), size_x, size_y]
    print('subplot = {0}'.format(subplot))
    f = FITSFigure(image['filename'], figure=figure, subplot=subplot)
    f.recenter(x_center, y_center, 0.95 * radius)
    set_hgps_style(f)
    f.show_colorscale(vmin=-1, vmax=8, stretch='power', exponent=1, cmap='jet') #vmid=-3, stretch='log', )
    # TODO: overplot sources  
#    f.show_regions("sources.reg")

filename = 'icrc2013_89_06.pdf'
print('Writing {}'.format(filename))
figure.savefig(filename)
