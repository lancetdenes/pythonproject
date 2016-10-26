import urllib
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

#downloads data from noaa historical buoy chart, extracts date, windspeed, air pressure and writes to file


def downloadbuoydata(url, outfname):
    
    content = urllib.urlopen(url)
    
    outfile = open(outfname, 'w')
    
    outfile.write('#month/day\thour:minute\twindspeed(meter/second)\tairpressure(hPa)\n')
    for line in content:
        if not line.startswith('#'):
            vals = line.strip().split()
            wdspd = vals[6]
            press = vals[12]
            month = vals[1]
            day = vals[2]
            hr = vals[3]
            minute = vals[4]
            outfile.write('%s/%s\t%s:%s\t%s\t%s\n' %(month, day, hr, minute, wdspd, press))


def plotdata(infile, outfile):
    windlist = []
    presslist = []
    i = 0
    for line in open(infile):
        if not line.startswith('#'):
            i += 1
            day, time, wdspd, pressure = line.strip().split('\t')
            if i % 5 == 0 and float(wdspd) < 40 and float(pressure) < 2000:
                windlist.append(wdspd)
                presslist.append(pressure)
    
    fig, ax1 = plt.subplots()
    ax1.plot(windlist, 'b')
    ax1.set_ylabel('windspeed', color='b')
    
    ax2 = ax1.twinx()
    ax2.plot(presslist, 'r')
    ax2.set_ylabel('pressure', color='r')
    
    plt.savefig(outfile)
    plt.close()



canaveral2015 = 'http://www.ndbc.noaa.gov/view_text_file.php?filename=41009h2015.txt.gz&dir=data/historical/stdmet/'
outf = '/ufrc/zoo6927/share/lancetdenes/pythonproject/canaveral2015.txt'

downloadbuoydata(canaveral2015, outf)
plotdata(outf, 'canav2015.jpg')
