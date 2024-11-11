#include "WiFi.h"
#include "esp_wifi.h"

typedef struct {
  unsigned frame_ctrl:16;
  unsigned duration_id:16;
  uint8_t addr1[6]; /* destination (or broadcast) address */
  uint8_t addr2[6]; /* source address */
  uint8_t addr3[6]; /* filtering address */
  unsigned seq_ctrl:16;
  uint8_t addr4[6]; /* optional */
} wifi_ieee80211_mac_hdr_t;

typedef struct {
  wifi_ieee80211_mac_hdr_t hdr;
  uint8_t payload[0]; /* network data ended with 4 bytes csum (CRC32) */
} wifi_ieee80211_packet_t;

wifi_promiscuous_filter_t filter = {
  .filter_mask = WIFI_PROMIS_FILTER_MASK_MGMT
};

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  esp_wifi_set_promiscuous(true);
  esp_wifi_set_promiscuous_filter(&filter);
  esp_wifi_set_promiscuous_rx_cb(&promiscuous_rx_callback);
  esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);  // You can set the desired channel
}

void loop() {
  // Nothing to do here, all work is done in the callback
}

void promiscuous_rx_callback(void* buf, wifi_promiscuous_pkt_type_t type) {
  if (type != WIFI_PKT_MGMT) return;

  wifi_promiscuous_pkt_t *pkt = (wifi_promiscuous_pkt_t *)buf;
  wifi_ieee80211_packet_t *ipkt = (wifi_ieee80211_packet_t *)pkt->payload;
  wifi_ieee80211_mac_hdr_t *hdr = &ipkt->hdr;

  // Only handle probe request packets
  if (hdr->frame_ctrl == 0x0040) {
    Serial.print("MAC: ");
    for (int i = 0; i < 6; i++) {
      Serial.printf("%02x", hdr->addr2[i]);
      if (i < 5) Serial.print(":");
    }
    Serial.print(" | RSSI: ");
    Serial.println(pkt->rx_ctrl.rssi);
  }
}
