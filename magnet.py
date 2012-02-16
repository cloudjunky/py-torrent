import libtorrent as lt
import time
import GeoIP

gi = GeoIP.open("./GeoIPCity.dat",GeoIP.GEOIP_STANDARD)

ses = lt.session()

params = { 'save_path': './'}

tfile = open('complete','r')

err = 0

def get_metadata(handle):
 print "Handle"
 print handle.trackers()

def get_peer_details(handle):


hash_array = ['85e54b554ef2f68ba675b0ffd2e96013451ffc46','1d204862cd639f1ef6baaf1a89afdfab9274a926','099774cef0302155d8172e2e2231de73d8fb586e','a60e0022419f4601bdda7c98bd5e99fee29c074f']
#for line in tfile:
for line in hash_array:
  h = line.split('|')
  torrent_hash = h[len(h)-1]

  link = "magnet:?xt=urn:btih:%s&tr=udp%%3A%%2F%%2Ftracker.openbittorrent.com%%3A80&tr=udp%%3A%%2F%%2Ftracker.publicbt.com%%3A80" % torrent_hash

  handle = lt.add_magnet_uri(ses, link, params)
  get_metadata(handle)

  print 'downloading metadata...'
  while (not handle.has_metadata()):
    print err
    time.sleep(1)
    err = err + 1

  print 'got metadata, starting torrent download...'
  files = handle.get_torrent_info()

  #Get tracker information
  for t in handle.trackers():
    print t

  #Get file information
  print "##### FILE INFO #####"
  files = handle.get_torrent_info()
  print "Total Files:%d" % files.num_files()
  for f in files.files():
    print "File Base:%s" % f.path
    print "File Size:%f" % (f.size/1024)

  #Get torrent summary information
  status = handle.status()
  print "Peers:", status.list_peers
  print "Num Peers:", status.num_peers
  print "Seeds:", status.list_seeds
  print "Num Seeds:", status.num_seeds
  print "Active:", status.active_time
  print "All Time Downloaded:", status.all_time_download

  #Get peer information
  pe = handle.get_peer_info()
  print "Peers: %d" % len(pe)

  for p in handle.get_peer_info():
    #print "Client:%s IP:%s Progress:%s" % (p.client,p.ip,p.downloading_total)
    gir = gi.record_by_addr(p.ip[0])
    if gir != None:
    #  print "%s %s" % (gir['country_name'], gir['city'])
    #print p.flags
    #print p.down_speed
    #print p.last_active
    #print p.downloading_progress
    #print p.pieces
    #print p.rtt
    #print p.total_download
    #print p.total_upload

  #while (handle.status().state != lt.torrent_status.seeding):
  #    print '%d %% done' % (handle.status().progress*100)
  #    for p in handle.get_peer_info():
  #      print p.ip
  #      print p.flags
      if 0:
          print p.down_speed
          print p.last_active
          print p.downloading_progress
          #print p.pieces
          print p.rtt
          print p.total_download
          print p.total_upload

          time.sleep(10)
