'use client';

import React, { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import Keycloak, { KeycloakConfig } from 'keycloak-js';

// Das Interface und der Context bleiben unverändert
interface IKeycloakContext {
    keycloak: Keycloak | null;
    isAuthenticated: boolean;
}
const KeycloakContext = createContext<IKeycloakContext | undefined>(undefined);

// Der benutzerdefinierte Hook bleibt unverändert
export const useKeycloak = () => {
    const context = useContext(KeycloakContext);
    if (!context) {
        throw new Error('useKeycloak must be used within a KeycloakProvider');
    }
    return context;
};

// Die Provider-Komponente mit der neuen, refaktorisierten Logik
export const KeycloakProvider = ({ children }: { children: ReactNode }) => {
    const [keycloak, setKeycloak] = useState<Keycloak | null>(null);
    const [isAuthenticated, setAuthenticated] = useState(false);

    useEffect(() => {
        // Konfiguration aus den Next.js Umgebungsvariablen laden
        // (Angepasst von import.meta.env zu process.env)
        const keycloakConfig: KeycloakConfig = {
            url: "auth.storasense.de",
            realm: "storasense-realm",
            clientId: "frontend-client",
        };

        const keycloakInstance = new Keycloak(keycloakConfig);

        console.log("Initializing Keycloak with new promise structure...");

        // Die neue Initialisierungslogik aus Ihrem Beispiel,
        // kombiniert mit unserer Lösung für den Silent Check.
        keycloakInstance.init({
            onLoad: 'check-sso',
            // WICHTIG: Diese Zeile ist entscheidend, um das Hängenbleiben zu verhindern!
            silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html',
        })
        .then((authenticated: boolean) => {
            console.log(`User is ${authenticated ? 'authenticated' : 'not authenticated'}.`);
            setAuthenticated(authenticated);
        })
        .catch((error) => {
            console.error('Keycloak initialization failed:', error);
            setAuthenticated(false);
        })
        .finally(() => {
            // Setzt die Keycloak-Instanz, nachdem der Prozess abgeschlossen ist
            console.log('Keycloak instance is now available.');
            setKeycloak(keycloakInstance);
        });

    }, []); // Leeres Array, damit es nur einmal beim Mounten ausgeführt wird

    const contextValue = { keycloak, isAuthenticated };

    return (
        <KeycloakContext.Provider value={contextValue}>
            {children}
        </KeycloakContext.Provider>
    );
};
