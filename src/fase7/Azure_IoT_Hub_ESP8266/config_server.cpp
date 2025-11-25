#include "config_server.h"

#include <cstring>

#if ENABLE_HTTP_CONFIG_SERVER
#include <EEPROM.h>
#include <ESP8266WebServer.h>
#include <ESP8266WiFi.h>
#endif

namespace
{
static void copyLiteral(const char* source, char* destination, size_t length)
{
  if (destination == nullptr || length == 0)
  {
    return;
  }

  if (source == nullptr)
  {
    destination[0] = '\0';
    return;
  }

  strncpy(destination, source, length - 1);
  destination[length - 1] = '\0';
}

#if ENABLE_HTTP_CONFIG_SERVER
static bool eeprom_ready = false;
static constexpr uint32_t CONFIG_MAGIC = 0x41495A31; // 'AIZ1'

typedef struct PersistedConfig
{
  uint32_t magic;
  uint16_t version;
  DeviceConfig config;
} PersistedConfig;

static constexpr size_t EEPROM_SIZE = sizeof(PersistedConfig);

static void ensureEeprom()
{
  if (!eeprom_ready)
  {
    EEPROM.begin(EEPROM_SIZE);
    eeprom_ready = true;
  }
}

static void writePersistedConfig(const DeviceConfig& config)
{
  PersistedConfig persisted = { CONFIG_MAGIC, static_cast<uint16_t>(IOT_CONFIG_STORAGE_VERSION), config };
  EEPROM.put(0, persisted);
  EEPROM.commit();
}
#endif
}

void device_config_load(DeviceConfig* config)
{
  if (config == nullptr)
  {
    return;
  }

  copyLiteral(IOT_CONFIG_WIFI_SSID, config->wifi_ssid, sizeof(config->wifi_ssid));
  copyLiteral(IOT_CONFIG_WIFI_PASSWORD, config->wifi_password, sizeof(config->wifi_password));
  copyLiteral(IOT_CONFIG_IOTHUB_FQDN, config->iothub_host, sizeof(config->iothub_host));
  copyLiteral(IOT_CONFIG_DEVICE_ID, config->device_id, sizeof(config->device_id));
  copyLiteral(IOT_CONFIG_DEVICE_KEY, config->device_key, sizeof(config->device_key));
  copyLiteral(IOT_CONFIG_DEVICE_LATITUDE, config->latitude, sizeof(config->latitude));
  copyLiteral(IOT_CONFIG_DEVICE_LONGITUDE, config->longitude, sizeof(config->longitude));

#if ENABLE_HTTP_CONFIG_SERVER
  ensureEeprom();
  PersistedConfig persisted;
  EEPROM.get(0, persisted);
  if (persisted.magic == CONFIG_MAGIC
      && persisted.version == IOT_CONFIG_STORAGE_VERSION)
  {
    *config = persisted.config;
  }
  else
  {
    writePersistedConfig(*config);
  }
#endif
}

void device_config_save(const DeviceConfig* config)
{
#if ENABLE_HTTP_CONFIG_SERVER
  if (config == nullptr)
  {
    return;
  }

  ensureEeprom();
  writePersistedConfig(*config);
#else
  (void)config;
#endif
}

#if ENABLE_HTTP_CONFIG_SERVER
namespace
{
static ESP8266WebServer config_server(80);
static DeviceConfig* active_config = nullptr;
static bool server_initialized = false;
static bool reconnect_requested = false;

static void copyArgumentToBuffer(const String& value, char* destination, size_t length)
{
  if (destination == nullptr || length == 0)
  {
    return;
  }

  value.toCharArray(destination, length);
  destination[length - 1] = '\0';
}

static String buildPage(const String& status_message)
{
  String page = F("<!DOCTYPE html><html lang='pt-br'><head><meta charset='utf-8'/><title>Configuração ESP8266</title><style>body{font-family:Arial;margin:0;padding:20px;background:#f2f2f2;}h1{margin-top:0;}form{background:#fff;padding:20px;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,0.1);}label{display:block;margin-top:10px;font-weight:bold;}input{width:100%;padding:8px;margin-top:4px;border:1px solid #ccc;border-radius:4px;}button{margin-top:20px;padding:10px 16px;border:none;background:#0078d4;color:#fff;border-radius:4px;cursor:pointer;}button:hover{background:#005a9e;}p.status{padding:10px;background:#e6f4ff;border:1px solid #90c9ff;border-radius:4px;}</style></head><body><h1>Configuração do dispositivo</h1>");
  if (status_message.length() > 0)
  {
    page += F("<p class='status'>");
    page += status_message;
    page += F("</p>");
  }

  page += F("<form method='POST' action='/save'>");
  page += F("<label>WiFi SSID</label><input name='wifi_ssid' value='");
  page += active_config->wifi_ssid;
  page += F("' />");
  page += F("<label>WiFi Password</label><input name='wifi_password' type='password' value='");
  page += active_config->wifi_password;
  page += F("' />");
  page += F("<label>IoT Hub Host</label><input name='iothub_host' value='");
  page += active_config->iothub_host;
  page += F("' />");
  page += F("<label>Device ID</label><input name='device_id' value='");
  page += active_config->device_id;
  page += F("' />");
  page += F("<label>Device Key</label><input name='device_key' type='password' value='");
  page += active_config->device_key;
  page += F("' />");
  page += F("<label>Latitude</label><input name='latitude' value='");
  page += active_config->latitude;
  page += F("' />");
  page += F("<label>Longitude</label><input name='longitude' value='");
  page += active_config->longitude;
  page += F("' />");
  page += F("<button type='submit'>Salvar</button></form></body></html>");
  return page;
}

static void handleRoot()
{
  config_server.send(200, "text/html", buildPage(String()));
}

static void handleSave()
{
  if (active_config == nullptr)
  {
    config_server.send(500, "text/plain", "Configuração indisponível");
    return;
  }

  if (config_server.hasArg("wifi_ssid"))
  {
    copyArgumentToBuffer(config_server.arg("wifi_ssid"), active_config->wifi_ssid, sizeof(active_config->wifi_ssid));
  }
  if (config_server.hasArg("wifi_password"))
  {
    copyArgumentToBuffer(config_server.arg("wifi_password"), active_config->wifi_password, sizeof(active_config->wifi_password));
  }
  if (config_server.hasArg("iothub_host"))
  {
    copyArgumentToBuffer(config_server.arg("iothub_host"), active_config->iothub_host, sizeof(active_config->iothub_host));
  }
  if (config_server.hasArg("device_id"))
  {
    copyArgumentToBuffer(config_server.arg("device_id"), active_config->device_id, sizeof(active_config->device_id));
  }
  if (config_server.hasArg("device_key"))
  {
    copyArgumentToBuffer(config_server.arg("device_key"), active_config->device_key, sizeof(active_config->device_key));
  }
  if (config_server.hasArg("latitude"))
  {
    copyArgumentToBuffer(config_server.arg("latitude"), active_config->latitude, sizeof(active_config->latitude));
  }
  if (config_server.hasArg("longitude"))
  {
    copyArgumentToBuffer(config_server.arg("longitude"), active_config->longitude, sizeof(active_config->longitude));
  }

  ensureEeprom();
  writePersistedConfig(*active_config);

  reconnect_requested = true;
  config_server.send(
      200,
      "text/html",
      buildPage(String("Configurações salvas. O dispositivo irá se reconectar automaticamente.")));
}
}

void config_server_begin(DeviceConfig* config)
{
  active_config = config;
  if (server_initialized || config == nullptr || !WiFi.isConnected())
  {
    return;
  }

  ensureEeprom();

  config_server.on("/", HTTP_GET, handleRoot);
  config_server.on("/save", HTTP_POST, handleSave);
  config_server.onNotFound([]() { config_server.send(404, "text/plain", "Not found"); });
  config_server.begin();
  server_initialized = true;

  Serial.print("Portal de configuração disponível em http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
}

void config_server_handle()
{
  if (!server_initialized || !WiFi.isConnected())
  {
    return;
  }

  config_server.handleClient();
}

bool config_server_should_reconnect()
{
  return reconnect_requested;
}

void config_server_clear_reconnect_flag()
{
  reconnect_requested = false;
}

#else  // ENABLE_HTTP_CONFIG_SERVER == 0

void config_server_begin(DeviceConfig* config)
{
  (void)config;
}

void config_server_handle() {}

bool config_server_should_reconnect() { return false; }

void config_server_clear_reconnect_flag() {}

#endif
