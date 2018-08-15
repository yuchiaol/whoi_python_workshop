def read_data(pr_file, month):
    """ Read precipitation nc-file """

    cube = iris.load_cube(pr_file, 'precipitation_flux')
    iris.coord_categorisation.add_month(cube, 'time')
    cube = cube.extract(iris.Constraint(month=month))

    return cube

def convert_pr_units(cube):
    """ Convert kg m-2 s-1 to mm day-1 """

    cube.data = cube.data * 86400
    cube.units = 'mm/day'

    return cube

def plot_data(cube, month, gridlines=False, levels=None):
    """Plot the data."""
       
    fig = plt.figure(figsize=[12,5])    
    iplt.contourf(cube, cmap=cmocean.cm.haline_r, 
                  levels=levels,
                  extend='max')

    plt.gca().coastlines()
    if gridlines:
        plt.gca().gridlines()
    cbar = plt.colorbar()
    cbar.set_label(str(cube.units))
   
    title = '%s precipitation climatology (%s)' %(cube.attributes['model_id'], month)
    plt.title(title)


import iris
import matplotlib.pyplot as plt
import iris.plot as iplt
import iris.coord_categorisation
import cmocean
import numpy
import argparse

import warnings
warnings.filterwarnings('ignore')

import pdb

import calendar

#help(plot_pr_climatology)

#plot_pr_climatology('data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc', 'Nov', gridlines=False)
#plt.show()

def main(inargs):
    """Run the program."""

    cube = read_data(inargs.infile, inargs.month)    
#    pdb.set_trace()
    cube = convert_pr_units(cube)
    clim = cube.collapsed('time', iris.analysis.MEAN)
    plot_data(clim, inargs.month, inargs.gridlines, levels=inargs.cbar_levels)
    plt.savefig(inargs.outfile)


if __name__ == '__main__':
    description='Plot the precipitation climatology for a given month.'
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("infile", type=str, help="Input file name")
#    parser.add_argument("month", type=str, help="Month to plot")
    parser.add_argument("month", type=str, choices=calendar.month_abbr[1:], help="Month to plot")
    parser.add_argument("outfile", type=str, help="Output file name")

    parser.add_argument("--gridlines", action="store_true", default=False,
                        help="Include gridlines on the plot")

    parser.add_argument("--cbar_levels", type=float, nargs='*', default=None,
                        help='list of levels / tick marks to appear on the colourbar')

    args = parser.parse_args()
    
    main(args)



