/**
 * Settings Screen - App configuration and preferences
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  Alert,
  Linking,
} from 'react-native';
import {
  Text,
  Card,
  Switch,
  Button,
  Divider,
  List,
  Surface,
} from 'react-native-paper';
import { useTranslation } from 'react-i18next';
import Icon from 'react-native-vector-icons/MaterialIcons';
import AsyncStorage from '@react-native-async-storage/async-storage';

import AIProcessor from '../services/AIProcessor';
import { colors, spacing, typography, shadows } from '../styles/theme';

const SettingsScreen: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [darkMode, setDarkMode] = useState(false);
  const [notifications, setNotifications] = useState(true);
  const [autoSave, setAutoSave] = useState(true);
  const [language, setLanguage] = useState(i18n.language);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const settings = await AsyncStorage.getItem('app_settings');
      if (settings) {
        const parsed = JSON.parse(settings);
        setDarkMode(parsed.darkMode || false);
        setNotifications(parsed.notifications !== false);
        setAutoSave(parsed.autoSave !== false);
      }
    } catch (error) {
      console.error('Error loading settings:', error);
    }
  };

  const saveSettings = async (newSettings: any) => {
    try {
      const currentSettings = {
        darkMode,
        notifications,
        autoSave,
        ...newSettings,
      };
      await AsyncStorage.setItem('app_settings', JSON.stringify(currentSettings));
    } catch (error) {
      console.error('Error saving settings:', error);
    }
  };

  const handleLanguageChange = () => {
    Alert.alert(
      'Change Language',
      'Select your preferred language',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'English',
          onPress: () => {
            i18n.changeLanguage('en');
            setLanguage('en');
          },
        },
        {
          text: 'العربية',
          onPress: () => {
            i18n.changeLanguage('ar');
            setLanguage('ar');
          },
        },
      ]
    );
  };

  const handleClearCache = () => {
    Alert.alert(
      'Clear Cache',
      'This will clear all cached analysis results. Are you sure?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Clear',
          style: 'destructive',
          onPress: async () => {
            try {
              await AsyncStorage.removeItem('analysis_results');
              Alert.alert('Success', 'Cache cleared successfully');
            } catch (error) {
              Alert.alert('Error', 'Failed to clear cache');
            }
          },
        },
      ]
    );
  };

  const handleResetSettings = () => {
    Alert.alert(
      'Reset Settings',
      'This will reset all settings to default values. Are you sure?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Reset',
          style: 'destructive',
          onPress: async () => {
            try {
              await AsyncStorage.removeItem('app_settings');
              setDarkMode(false);
              setNotifications(true);
              setAutoSave(true);
              i18n.changeLanguage('en');
              setLanguage('en');
              Alert.alert('Success', 'Settings reset successfully');
            } catch (error) {
              Alert.alert('Error', 'Failed to reset settings');
            }
          },
        },
      ]
    );
  };

  const handleAbout = () => {
    Alert.alert(
      'About Sperm Analyzer AI',
      `Version: 1.0.0
      
Revolutionary AI-powered sperm analysis application using YOLOv8 + DeepSORT for real-time detection and tracking.

Features:
• 100% Offline Analysis
• Real AI Models (No Simulation)
• CASA Metrics Calculation
• Multi-language Support
• Professional Reports

Developed by: Youssef Shtaiwi
AI & Mobile Development Expert

Built: July 2025`,
      [{ text: 'OK' }]
    );
  };

  const handleContactDeveloper = () => {
    Alert.alert(
      'Contact Developer',
      'Choose how to contact the developer:',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Email',
          onPress: () => Linking.openURL('mailto:youssef@spermanalyzer.ai'),
        },
        {
          text: 'GitHub',
          onPress: () => Linking.openURL('https://github.com/youssefshtaiwi'),
        },
      ]
    );
  };

  const settingSections = [
    {
      title: 'Preferences',
      items: [
        {
          title: t('language'),
          subtitle: language === 'ar' ? 'العربية' : 'English',
          icon: 'language',
          onPress: handleLanguageChange,
        },
        {
          title: 'Dark Mode',
          subtitle: 'Use dark theme',
          icon: 'dark-mode',
          rightComponent: (
            <Switch
              value={darkMode}
              onValueChange={(value) => {
                setDarkMode(value);
                saveSettings({ darkMode: value });
              }}
            />
          ),
        },
        {
          title: 'Notifications',
          subtitle: 'Enable push notifications',
          icon: 'notifications',
          rightComponent: (
            <Switch
              value={notifications}
              onValueChange={(value) => {
                setNotifications(value);
                saveSettings({ notifications: value });
              }}
            />
          ),
        },
        {
          title: 'Auto Save Results',
          subtitle: 'Automatically save analysis results',
          icon: 'save',
          rightComponent: (
            <Switch
              value={autoSave}
              onValueChange={(value) => {
                setAutoSave(value);
                saveSettings({ autoSave: value });
              }}
            />
          ),
        },
      ],
    },
    {
      title: 'AI Model',
      items: [
        {
          title: 'Model Status',
          subtitle: AIProcessor.isModelLoaded() ? 'Loaded' : 'Not Loaded',
          icon: 'psychology',
          rightComponent: (
            <Text style={[
              styles.statusText,
              { color: AIProcessor.isModelLoaded() ? colors.success : colors.error }
            ]}>
              {AIProcessor.isModelLoaded() ? '✅' : '❌'}
            </Text>
          ),
        },
        {
          title: 'Model Path',
          subtitle: AIProcessor.getModelPath() || 'Not available',
          icon: 'folder',
        },
        {
          title: 'Offline Mode',
          subtitle: '100% offline processing',
          icon: 'offline-bolt',
          rightComponent: (
            <Text style={[styles.statusText, { color: colors.success }]}>
              ✅
            </Text>
          ),
        },
      ],
    },
    {
      title: 'Data Management',
      items: [
        {
          title: 'Clear Cache',
          subtitle: 'Remove cached analysis results',
          icon: 'clear-all',
          onPress: handleClearCache,
        },
        {
          title: 'Export Data',
          subtitle: 'Export all analysis results',
          icon: 'file-download',
          onPress: () => Alert.alert('Info', 'Export functionality coming soon'),
        },
        {
          title: 'Reset Settings',
          subtitle: 'Reset all settings to default',
          icon: 'restore',
          onPress: handleResetSettings,
        },
      ],
    },
    {
      title: 'Support',
      items: [
        {
          title: 'About',
          subtitle: 'App information and version',
          icon: 'info',
          onPress: handleAbout,
        },
        {
          title: 'Contact Developer',
          subtitle: 'Get in touch with the developer',
          icon: 'contact-mail',
          onPress: handleContactDeveloper,
        },
        {
          title: 'Rate App',
          subtitle: 'Rate us on the app store',
          icon: 'star-rate',
          onPress: () => Alert.alert('Info', 'Rating functionality coming soon'),
        },
      ],
    },
  ];

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Header */}
      <Surface style={styles.header}>
        <Text style={styles.headerTitle}>⚙️ Settings</Text>
        <Text style={styles.headerSubtitle}>
          Configure your app preferences
        </Text>
      </Surface>

      {/* Settings Sections */}
      {settingSections.map((section, sectionIndex) => (
        <View key={sectionIndex} style={styles.section}>
          <Text style={styles.sectionTitle}>{section.title}</Text>
          <Card style={styles.sectionCard}>
            {section.items.map((item, itemIndex) => (
              <View key={itemIndex}>
                <List.Item
                  title={item.title}
                  description={item.subtitle}
                  left={(props) => (
                    <List.Icon
                      {...props}
                      icon={({ size, color }) => (
                        <Icon name={item.icon} size={size} color={color} />
                      )}
                    />
                  )}
                  right={() => item.rightComponent || (
                    item.onPress ? (
                      <Icon name="chevron-right" size={24} color={colors.textSecondary} />
                    ) : null
                  )}
                  onPress={item.onPress}
                  style={styles.listItem}
                />
                {itemIndex < section.items.length - 1 && (
                  <Divider style={styles.divider} />
                )}
              </View>
            ))}
          </Card>
        </View>
      ))}

      {/* System Information */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>System Information</Text>
        <Card style={styles.sectionCard}>
          <Card.Content>
            <View style={styles.systemInfo}>
              <View style={styles.systemRow}>
                <Text style={styles.systemLabel}>App Version:</Text>
                <Text style={styles.systemValue}>1.0.0</Text>
              </View>
              <View style={styles.systemRow}>
                <Text style={styles.systemLabel}>Build Date:</Text>
                <Text style={styles.systemValue}>July 2025</Text>
              </View>
              <View style={styles.systemRow}>
                <Text style={styles.systemLabel}>AI Model:</Text>
                <Text style={styles.systemValue}>YOLOv8 + DeepSORT</Text>
              </View>
              <View style={styles.systemRow}>
                <Text style={styles.systemLabel}>Platform:</Text>
                <Text style={styles.systemValue}>React Native</Text>
              </View>
              <View style={styles.systemRow}>
                <Text style={styles.systemLabel}>Developer:</Text>
                <Text style={styles.systemValue}>Youssef Shtaiwi</Text>
              </View>
            </View>
          </Card.Content>
        </Card>
      </View>

      {/* Footer */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>
          Sperm Analyzer AI
        </Text>
        <Text style={styles.footerSubtext}>
          Revolutionary AI-Powered Fertility Diagnostics
        </Text>
        <Text style={styles.footerVersion}>
          Version 1.0.0 • Built with ❤️ by Youssef Shtaiwi
        </Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    padding: spacing.lg,
    margin: spacing.lg,
    borderRadius: 12,
    ...shadows.small,
  },
  headerTitle: {
    ...typography.h3,
    color: colors.text,
    textAlign: 'center',
    marginBottom: spacing.xs,
  },
  headerSubtitle: {
    ...typography.body2,
    color: colors.textSecondary,
    textAlign: 'center',
  },
  section: {
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
  },
  sectionTitle: {
    ...typography.h4,
    color: colors.text,
    marginBottom: spacing.md,
  },
  sectionCard: {
    ...shadows.small,
  },
  listItem: {
    paddingVertical: spacing.sm,
  },
  divider: {
    marginLeft: 56,
  },
  statusText: {
    ...typography.body1,
    fontWeight: '600',
  },
  systemInfo: {
    gap: spacing.sm,
  },
  systemRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  systemLabel: {
    ...typography.body2,
    color: colors.text,
  },
  systemValue: {
    ...typography.body2,
    color: colors.textSecondary,
    fontWeight: '500',
  },
  footer: {
    alignItems: 'center',
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.xl,
  },
  footerText: {
    ...typography.h4,
    color: colors.text,
    marginBottom: spacing.xs,
  },
  footerSubtext: {
    ...typography.body2,
    color: colors.textSecondary,
    textAlign: 'center',
    marginBottom: spacing.sm,
  },
  footerVersion: {
    ...typography.caption,
    color: colors.textSecondary,
    textAlign: 'center',
  },
});

export default SettingsScreen;
