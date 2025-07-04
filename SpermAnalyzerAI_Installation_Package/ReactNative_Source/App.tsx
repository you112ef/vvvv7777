/**
 * Sperm Analyzer AI Mobile App
 * Main application component
 */

import React from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Alert
} from 'react-native';

const App: React.FC = () => {
  
  const showAnalysisDemo = () => {
    Alert.alert(
      'Sperm Analysis Demo',
      'AI-powered sperm analysis system ready!\n\n' +
      '✅ Camera integration\n' +
      '✅ Real-time AI analysis\n' +
      '✅ CASA metrics calculation\n' +
      '✅ Multi-language support\n' +
      '✅ Graph visualization\n\n' +
      'Connect to backend server to start analysis.',
      [{text: 'OK', style: 'default'}]
    );
  };

  const showFeatures = () => {
    Alert.alert(
      'App Features',
      '🧬 Sperm Analyzer AI\n\n' +
      '🔬 Real AI Analysis (YOLOv8 + DeepSORT)\n' +
      '📱 Mobile Camera Integration\n' +
      '📊 Interactive Graphs\n' +
      '🌍 Multi-language (AR/EN)\n' +
      '⚡ Real-time Processing\n' +
      '📋 Clinical Reports\n\n' +
      'Built by Youssef Shtaiwi',
      [{text: 'Amazing!', style: 'default'}]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar 
        barStyle="light-content" 
        backgroundColor="#1565C0"
      />
      <ScrollView contentInsetAdjustmentBehavior="automatic">
        
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>🧬 Sperm Analyzer AI</Text>
          <Text style={styles.subtitle}>
            Revolutionary AI-Powered Fertility Diagnostics
          </Text>
          <Text style={styles.version}>Version 1.0.0</Text>
        </View>

        {/* Main Content */}
        <View style={styles.content}>
          
          {/* Features Section */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>📱 Mobile App Features</Text>
            
            <View style={styles.featureCard}>
              <Text style={styles.featureTitle}>🔬 AI-Powered Analysis</Text>
              <Text style={styles.featureDesc}>
                Real-time sperm detection and tracking using YOLOv8 + DeepSORT
              </Text>
            </View>
            
            <View style={styles.featureCard}>
              <Text style={styles.featureTitle}>📸 Camera Integration</Text>
              <Text style={styles.featureDesc}>
                Capture photos and videos directly from your device camera
              </Text>
            </View>
            
            <View style={styles.featureCard}>
              <Text style={styles.featureTitle}>📊 Interactive Graphs</Text>
              <Text style={styles.featureDesc}>
                Visualize analysis results with charts and statistics
              </Text>
            </View>
            
            <View style={styles.featureCard}>
              <Text style={styles.featureTitle}>🌍 Multi-Language</Text>
              <Text style={styles.featureDesc}>
                English and Arabic support with RTL layout
              </Text>
            </View>
          </View>

          {/* Action Buttons */}
          <View style={styles.buttonSection}>
            <TouchableOpacity 
              style={[styles.button, styles.primaryButton]}
              onPress={showAnalysisDemo}
            >
              <Text style={styles.buttonText}>🔬 Start Analysis Demo</Text>
            </TouchableOpacity>
            
            <TouchableOpacity 
              style={[styles.button, styles.secondaryButton]}
              onPress={showFeatures}
            >
              <Text style={[styles.buttonText, styles.secondaryButtonText]}>
                ℹ️ View All Features
              </Text>
            </TouchableOpacity>
          </View>

          {/* Status Section */}
          <View style={styles.statusSection}>
            <Text style={styles.statusTitle}>🚀 System Status</Text>
            <View style={styles.statusRow}>
              <Text style={styles.statusLabel}>Mobile App:</Text>
              <Text style={styles.statusActive}>✅ Active</Text>
            </View>
            <View style={styles.statusRow}>
              <Text style={styles.statusLabel}>AI Models:</Text>
              <Text style={styles.statusReady}>🟡 Ready</Text>
            </View>
            <View style={styles.statusRow}>
              <Text style={styles.statusLabel}>Backend:</Text>
              <Text style={styles.statusPending}>🔄 Connect Required</Text>
            </View>
          </View>

          {/* Developer Info */}
          <View style={styles.footer}>
            <Text style={styles.footerText}>
              Developed by Youssef Shtaiwi
            </Text>
            <Text style={styles.footerSubtext}>
              AI & Mobile Development Expert
            </Text>
            <Text style={styles.footerDate}>
              Built: July 4, 2025
            </Text>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  header: {
    backgroundColor: '#1565C0',
    padding: 30,
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#E3F2FD',
    textAlign: 'center',
    marginBottom: 4,
  },
  version: {
    fontSize: 14,
    color: '#BBDEFB',
    textAlign: 'center',
  },
  content: {
    padding: 20,
  },
  section: {
    marginBottom: 30,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#1565C0',
    marginBottom: 15,
  },
  featureCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 12,
    marginBottom: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  featureTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  featureDesc: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  buttonSection: {
    marginBottom: 30,
  },
  button: {
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 25,
    alignItems: 'center',
    marginBottom: 12,
  },
  primaryButton: {
    backgroundColor: '#1565C0',
  },
  secondaryButton: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: '#1565C0',
  },
  buttonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: 'white',
  },
  secondaryButtonText: {
    color: '#1565C0',
  },
  statusSection: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 12,
    marginBottom: 30,
    elevation: 2,
  },
  statusTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  statusRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  statusLabel: {
    fontSize: 14,
    color: '#666',
  },
  statusActive: {
    fontSize: 14,
    color: '#4CAF50',
    fontWeight: 'bold',
  },
  statusReady: {
    fontSize: 14,
    color: '#FF9800',
    fontWeight: 'bold',
  },
  statusPending: {
    fontSize: 14,
    color: '#2196F3',
    fontWeight: 'bold',
  },
  footer: {
    alignItems: 'center',
    padding: 20,
  },
  footerText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  footerSubtext: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
  footerDate: {
    fontSize: 12,
    color: '#999',
  },
});

export default App;
