import libtorrent as lt
import time
import GeoIP
import pickle

def ip_location(ip_address):
  #Receive an and return Country, City and Latitude/Longitude
  gi = GeoIP.open("./GeoIPCity.dat",GeoIP.GEOIP_STANDARD)
  gir = gi.record_by_addr(ip_address)
  if gir != None:
    location = [gir['country_name'], gir['city']]
  return location

def read_hash_from_file(line):
  #Read a line from the file and return a hash.
  h = line.split('|')
  torrent_hash = h[len(h)-1]
  return torrent_hash

def total_hashes(f):
  #Read file and return how many hashes there are
  return num_hashes

def peer_info(handle):
  #Take the torrent handle and return peer information
  return 0

def create_magnet_url(torrent_hash):
  link = "magnet:?xt=urn:btih:%s&tr=udp%%3A%%2F%%2Ftracker.openbittorrent.com%%3A80&tr=udp%%3A%%2F%%2Ftracker.publicbt.com%%3A80" % torrent_hash
  return link

def create_session():
  ses = lt.session()
  return ses

def create_handle(ses,link,params):
  handle = lt.add_magnet_uri(ses, link, params)
  return handle

def get_metadata(handle):
  print 'downloading metadata...'
  handle.metadata()
  #while (not handle.has_metadata()):
  #  print err
  #  time.sleep(1)
  #  err = err + 1
  print 'got metadata, starting torrent download...'
  #return handle.metadata()

def get_tracker_information(handle):
  #Get tracker information
  for t in handle.trackers():
    print t

def get_file_information(handle):
  #Get file information
  print "##### FILE INFO #####"
  files = handle.get_torrent_info()
  print "Total Files:%d" % files.num_files()
  for f in files.files():
    print "File Path:%s" % f.path
    print "File Offset:%s" % f.offset
    print "File Size:%f" % (f.size/1024)

def get_torrent_summary_information(handle):
  #Get torrent summary information
  status = handle.status()
  print "Peers:", status.list_peers
  print "Num Peers:", status.num_peers
  print "Seeds:", status.list_seeds
  print "Num Seeds:", status.num_seeds
  print "Active:", status.active_time
  print "All Time Downloaded:", status.all_time_download
  print "File Information", get_file_information(handle)

def get_peer_details(handle):
  #Get peer information
  pe = handle.get_peer_info()
  print "Peers: %d" % len(pe)

  for p in handle.get_peer_info():
    print "Client:%s IP:%s Country:%s Progress:%s" % (p.client,p.ip,ip_location(p.ip[0]),p.downloading_total)
    #print p.flags
    #print p.down_speed
    #print p.last_active
    #print p.downloading_progress
    #print p.pieces
    #print p.rtt
    #print p.total_download
    #print p.total_upload

def download_torrent(handle):
  while (handle.status().state != lt.torrent_status.seeding):
    print '%d %% done' % (handle.status().progress*100)
    for p in handle.get_peer_info():
      print p.ip
      print p.flags
      print p.down_speed
      print p.last_active
      print p.downloading_progress
      #print p.pieces
      print p.rtt
      print p.total_download
      print p.total_upload


params = { 'save_path': './'}
num_tries = 3

torrent_file = 'complete'
pickle_file = 'top100.bin'

use_pickle = 1 

if pickle_file:
    f = pickle.load(open(pickle_file))
elif (not pickle_file):
    f = open(torrent_file,'r')

for line in f:
  #print line
  tries = 0
  # Create a session, get a handle, grab a hash and get peers
  if pickle_file:
      link = line['downloadLink']
  elif (not pickle_file):
      my_hash = read_hash_from_file(line)
      link = create_magnet_url(my_hash)

  print link
  ses = create_session()
  handle = create_handle(ses,link,params)

  while tries < num_tries:
  #  get_metadata(handle)
    print "Calling metadata"
    handle.has_metadata()
    time.sleep(30) #Give metadata 10s to timeout
    if (not handle.has_metadata()):
      tries = tries + 1
    else:
      print "Boom got metadata"
      #break
      #Print the file info
      files = get_file_information(handle)
      peers = get_peer_details(handle)
      print get_torrent_summary_information(handle)

print "done"
