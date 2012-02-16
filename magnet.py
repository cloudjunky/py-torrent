import libtorrent as lt
import time
import GeoIP

def ip_location(ip_address):
  #Receive an and return Country, City and Latitude/Longitude
  gi = GeoIP.open("./GeoIPCity.dat",GeoIP.GEOIP_STANDARD)
  gir = gi.record_by_addr(ip_address)
  if gir != None:
    location = [gir['country_name'], gir['city']]
  return location

def read_hash_from_file(f):
  #Read a line from the file and return a hash.
  #hash_array = ['85e54b554ef2f68ba675b0ffd2e96013451ffc46','1d204862cd639f1ef6baaf1a89afdfab9274a926','099774cef0302155d8172e2e2231de73d8fb586e','a60e0022419f4601bdda7c98bd5e99fee29c074f']
  #for line in hash_array:
  #  h = line.split('|')
  #  torrent_hash = h[len(h)-1]
  torrent_hash = "85e54b554ef2f68ba675b0ffd2e96013451ffc46"
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
  print handle
  err = 0
  print 'downloading metadata...'
  while (not handle.has_metadata()):
    print err
    time.sleep(1)
    err = err + 1
  print 'got metadata, starting torrent download...'
  files = handle.get_torrent_info()
  print files
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
    print "File Base:%s" % f.path
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

def get_peer_details(handle):
  #Get peer information
  pe = handle.get_peer_info()
  print "Peers: %d" % len(pe)

  for p in handle.get_peer_info():
    #print "Client:%s IP:%s Progress:%s" % (p.client,p.ip,p.downloading_total)
    gir = gi.record_by_addr(p.ip[0])
    if gir != None:
      print "%s %s" % (gir['country_name'], gir['city'])
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

# Create a session, get a handle, grab a hash and get peers
f = open('complete','r')
my_hash = read_hash_from_file(f)
link = create_magnet_url(my_hash)
print link
ses = create_session()
handle = create_handle(ses,link,params)
metadata = get_metadata(handle)
print "done"
