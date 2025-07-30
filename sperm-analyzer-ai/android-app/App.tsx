/**
 * Sperm Analyzer AI - Offline Mobile App
 * Real AI-powered sperm analysis with YOLOv8 + DeepSORT
 * Works 100% offline with embedded models
 */

import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Provider as PaperProvider } from 'react-native-paper';
import { StatusBar, Platform, PermissionsAndroid } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { I18nextProvider } from 'react-i18next';

// Screens
import HomeScreen from './src/screens/HomeScreen';
import CameraScreen from './src/screens/CameraScreen';
import AnalysisScreen from './src/screens/AnalysisScreen';
import ResultsScreen from './src/screens/ResultsScreen';
import SettingsScreen from './src/screens/SettingsScreen';

// Services
import i18n from './src/services/i18n';
import { theme } from './src/styles/theme';

const Tab = createBottomTabNavigator();

const App: React.FC = () => {
  
  useEffect(() => {
    requestPermissions();
  }, []);

  const requestPermissions = async () => {
    if (Platform.OS === 'android') {
      try {
        const grants = await PermissionsAndroid.requestMultiple([
          PermissionsAndroid.PERMISSIONS.CAMERA,
          PermissionsAndroid.PERMISSIONS.RECORD_AUDIO,
          PermissionsAndroid.PERMISSIONS.WRITE_EXTERNAL_STORAGE,
          PermissionsAndroid.PERMISSIONS.READ_EXTERNAL_STORAGE,
        ]);

        console.log('Permissions granted:', grants);
      } catch (err) {
        console.warn('Permission request error:', err);
      }
    }
  };

  return (
    <I18nextProvider i18n={i18n}>
      <PaperProvider theme={theme}>
        <StatusBar 
          barStyle="light-content" 
          backgroundColor={theme.colors.primary}
        />
        <NavigationContainer>
          <Tab.Navigator
            screenOptions={({ route }) => ({
              tabBarIcon: ({ focused, color, size }) => {
                let iconName: string;

                switch (route.name) {
                  case 'Home':
                    iconName = 'home';
                    break;
                  case 'Camera':
                    iconName = 'camera-alt';
                    break;
                  case 'Analysis':
                    iconName = 'analytics';
                    break;
                  case 'Results':
                    iconName = 'assessment';
                    break;
                  case 'Settings':
                    iconName = 'settings';
                    break;
                  default:
                    iconName = 'help';
                }

                return <Icon name={iconName} size={size} color={color} />;
              },
              tabBarActiveTintColor: theme.colors.primary,
              tabBarInactiveTintColor: 'gray',
              tabBarStyle: {
                backgroundColor: 'white',
                borderTopWidth: 1,
                borderTopColor: '#E0E0E0',
                height: 60,
                paddingBottom: 8,
                paddingTop: 8,
              },
              headerStyle: {
                backgroundColor: theme.colors.primary,
              },
              headerTintColor: 'white',
              headerTitleStyle: {
                fontWeight: 'bold',
              },
            })}
          >
            <Tab.Screen 
              name="Home" 
              component={HomeScreen}
              options={{ title: '🧬 Sperm Analyzer AI' }}
            />
            <Tab.Screen 
              name="Camera" 
              component={CameraScreen}
              options={{ title: '📸 Capture' }}
            />
            <Tab.Screen 
              name="Analysis" 
              component={AnalysisScreen}
              options={{ title: '🧠 AI Analysis' }}
            />
            <Tab.Screen 
              name="Results" 
              component={ResultsScreen}
              options={{ title: '📊 Results' }}
            />
            <Tab.Screen 
              name="Settings" 
              component={SettingsScreen}
              options={{ title: '⚙️ Settings' }}
            />
          </Tab.Navigator>
        </NavigationContainer>
      </PaperProvider>
    </I18nextProvider>
  );
};

export default App;
