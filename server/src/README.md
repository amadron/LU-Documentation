# DarkflameServer-Quellcode: Dokumentation

Dieser Ordner enthält **Dokumentation zum Quellcode**, nicht den Quellcode selbst. Der dokumentierte Quellstand ist im offiziellen [`DarkflameServer`-Repository](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/) verfügbar. Die ausführliche Architektur- und Repository-Übersicht steht in der [DarkflameServer Architecture and Repository Structure](../DarkflameServer%20Architecture%20and%20Repository%20Structure.md); Details zu Spielobjekten, Komponenten und Simulation enthält [World Simulation and Entity Model](../DarkflameServer%20World%20Simulation%20and%20Entity%20Model.md).

## Aufbau und Zuständigkeiten

| Quellcodepfad | Aufgabe |
| --- | --- |
| [`dMasterServer/`](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/) | Koordiniert Serverdienste, Spielwelten und Instanzen und startet Prozesse. |
| [`dAuthServer/`](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dAuthServer/) | Verarbeitet Authentifizierungs- und Anmeldeverkehr. |
| [`dChatServer/`](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dChatServer/) | Zuständig für Chat, Freunde, Teams und die optionale Chat-Web-API. |
| [`dWorldServer/`](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/) | Betreibt eine Zone, verarbeitet Spielverkehr und führt die Welt-Updates aus. |
| [`dNet/`](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/) | Gemeinsamer Netzwerktransport, Paketdefinitionen und Serialisierung. |
| [`dGame/`](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/) | Spielzustand und Spiellogik: Entities, Komponenten, Nachrichten, Inventar und Missionen. |
| [`dScripts/`](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dScripts/) | Native C++-Skripte für Spielinhalte und Zonen. |
| [`dZoneManager/`](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/) | Laden und Verwalten von Zonen, Szenen, Spawnern und Pfaden. |
| [`dDatabase/`](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/) | Zugriff auf Spiel- und Client-Datenbanken sowie Migrationen. |
| [`dCommon/`](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dCommon/), [`dPhysics/`](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dPhysics/), [`dNavigation/`](https://github.com/DarkflameUniverse/DarkflameServer/tree/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNavigation/) | Gemeinsame Hilfsfunktionen, Physiksimulation und Navigation. |

## Einstiegspunkte zum Lesen

- **Serverstart und Dienstkoordination:** [`MasterServer.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/MasterServer.cpp), [`Start.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/Start.cpp) und [`InstanceManager.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dMasterServer/InstanceManager.cpp).
- **Anmeldung und Weltprozess:** [`AuthServer.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dAuthServer/AuthServer.cpp) und [`WorldServer.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dWorldServer/WorldServer.cpp).
- **Netzwerk:** [`dServer.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dNet/dServer.cpp) und die für den jeweiligen Dienst zuständigen Paketdefinitionen und Handler.
- **Entities und Spielzustand:** [`Entity.h`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/Entity.h), [`EntityManager.h`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dGame/EntityManager.h) sowie die betroffenen Komponenten und Game Messages.
- **Zonenverhalten:** [`Zone.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dZoneManager/Zone.cpp) und die zugehörigen nativen Skripte in `dScripts/`.
- **Persistenz:** [`Database.cpp`](https://github.com/DarkflameUniverse/DarkflameServer/blob/8b7d1b946b5e7df18f2c82ccabcb2634aefc11f4/dDatabase/GameDatabase/Database.cpp), die betroffenen Tabelleninterfaces und Backend-Implementierungen.

## Grober Ablauf

Der `MasterServer` koordiniert Dienste und Weltinstanzen. `AuthServer` wickelt die Anmeldung ab, `ChatServer` stellt Chatfunktionen bereit, und ein `WorldServer` verarbeitet das Spielgeschehen einer Zone. Die Dienste tauschen Nachrichten über den gemeinsamen Netzwerkcode in `dNet/` aus. Im Weltprozess verwalten `dGame/` und `dZoneManager/` Spielobjekte und Zonen; Datenbankzugriffe laufen über `dDatabase/`.

Die Zuständigkeiten sind nicht immer auf eine einzelne Datei beschränkt: Verhalten kann zugleich von C++-Implementierung, Komponenten, Game Messages, nativen Skripten und Client-Daten abhängen. Für Änderungen sollte daher auch die jeweilige Registrierung und der Aufrufpfad geprüft werden.
