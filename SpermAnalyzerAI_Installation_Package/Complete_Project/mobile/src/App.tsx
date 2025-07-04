/**
 * Sperm Analyzer AI Mobile App
 * Main application component with navigation
 */

import React, {useEffect} from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {Provider as PaperProvider} from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialIcons';
import {useTranslation} from 'react-i18next';

import './src/services/i18n';
import {theme} from './src/styles/theme';
import HomeScreen from './src/screens/HomeScreen';
import CameraScreen from './src/screens/CameraScreen';
import AnalysisScreen from './src/screens/AnalysisScreen';
import GraphScreen from './src/screens/GraphScreen';
import SettingsScreen from './src/screens/SettingsScreen';

const Tab = createBottomTabNavigator();

const App: React.FC = () => {
  const {t, i18n} = useTranslation();

  return (
    <PaperProvider theme={theme}>
      <NavigationContainer>
        <Tab.Navigator
          screenOptions={({route}) => ({
            tabBarIcon: ({focused, color, size}) => {
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
                case 'Graphs':
                  iconName = 'bar-chart';
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
            tabBarInactiveTintColor: theme.colors.outline,
            tabBarStyle: {
              backgroundColor: theme.colors.surface,
              borderTopColor: theme.colors.outline,
            },
            headerStyle: {
              backgroundColor: theme.colors.primary,
            },
            headerTintColor: theme.colors.onPrimary,
          })}>
          <Tab.Screen 
            name="Home" 
            component={HomeScreen}
            options={{title: t('navigation.home')}}
          />
          <Tab.Screen 
            name="Camera" 
            component={CameraScreen}
            options={{title: t('navigation.camera')}}
          />
          <Tab.Screen 
            name="Analysis" 
            component={AnalysisScreen}
            options={{title: t('navigation.analysis')}}
          />
          <Tab.Screen 
            name="Graphs" 
            component={GraphScreen}
            options={{title: t('navigation.graphs')}}
          />
          <Tab.Screen 
            name="Settings" 
            component={SettingsScreen}
            options={{title: t('navigation.settings')}}
          />
        </Tab.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
};

export default App;
