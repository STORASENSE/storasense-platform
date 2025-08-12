import React, {
  createContext,
  useEffect,
  useState,
  useRef,
  ReactNode,
} from 'react';
import Keycloak, { KeycloakConfig } from 'keycloak-js';
import { useDispatch } from 'react-redux';
import { setToken } from '@/redux/slices/authSlice';

interface KeycloakContextProps {
  keycloak: Keycloak | null;
  authenticated: boolean;
}

const KeycloakContext = createContext<KeycloakContextProps | undefined>(
  undefined,
);

interface KeycloakProviderProps {
  children: ReactNode;
}

export const KeycloakProvider: React.FC<KeycloakProviderProps> = ({ children }) => {
  const isRun = useRef<boolean>(false);
  const [keycloak, setKeycloak] = useState<Keycloak | null>(null);
  const [authenticated, setAuthenticated] = useState<boolean>(false);
  const dispatch = useDispatch(); // useDispatch Hook

  useEffect(() => {
    if (isRun.current) return;
    isRun.current = true;

    const keycloakConfig: KeycloakConfig = {
      url: "https://auth.storasense.de",
      realm: "storasense-realm",
      clientId: "frontend-client",
    };
    const keycloakInstance = new Keycloak(keycloakConfig);

    keycloakInstance
      .init({
        onLoad: 'check-sso',
      })
      .then((authenticated: boolean) => {
        setAuthenticated(authenticated);
        if (authenticated) {
          // Write initial token to Redux store
          dispatch(setToken(keycloakInstance.token!));
        }
      })
      .catch((error) => {
        console.error('Keycloak initialization failed:', error);
        setAuthenticated(false);
      })
      .finally(() => {
        setKeycloak(keycloakInstance);
      });

    // Event-handler for token refresh
    keycloakInstance.onTokenExpired = () => {
      console.log("Keycloak token expired. Attempting to refresh...");
      keycloakInstance.updateToken(30) // Try to refresh the token 30 seconds before it expires
        .then((refreshed) => {
          if (refreshed) {
            console.log("Token refreshed successfully.");
            // Update the new token in the Redux store
            dispatch(setToken(keycloakInstance.token!));
          } else {
            console.warn('Token could not be refreshed, session may have expired.');
          }
        }).catch(() => {
          console.error('Failed to refresh token.');
        });
    };
  }, [dispatch]);

  return (
    <KeycloakContext.Provider value={{ keycloak, authenticated }}>
      {children}
    </KeycloakContext.Provider>
  );
};

export { KeycloakContext };
