/**
 * Camera Screen - Photo and video capture
 */

import React, { useState, useRef, useCallback } from 'react';
import {
  View,
  StyleSheet,
  Alert,
  Dimensions,
  TouchableOpacity,
} from 'react-native';
import {
  Button,
  Text,
  Surface,
  ActivityIndicator,
  Card,
} from 'react-native-paper';
import { useTranslation } from 'react-i18next';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { launchImageLibrary, launchCamera, MediaType } from 'react-native-image-picker';
import DocumentPicker from 'react-native-document-picker';

import { colors, spacing, typography, shadows } from '../styles/theme';

const { width, height } = Dimensions.get('window');

const CameraScreen: React.FC = ({ navigation }: any) => {
  const { t } = useTranslation();
  const [isRecording, setIsRecording] = useState(false);
  const [selectedMedia, setSelectedMedia] = useState<string | null>(null);
  const [mediaType, setMediaType] = useState<'photo' | 'video' | null>(null);

  const handleTakePhoto = useCallback(() => {
    const options = {
      mediaType: 'photo' as MediaType,
      quality: 1,
      includeBase64: false,
    };

    launchCamera(options, (response) => {
      if (response.assets && response.assets[0]) {
        const asset = response.assets[0];
        setSelectedMedia(asset.uri || null);
        setMediaType('photo');
        
        Alert.alert(
          'Photo Captured',
          'Would you like to analyze this photo?',
          [
            { text: 'Cancel', style: 'cancel' },
            { 
              text: 'Analyze', 
              onPress: () => {
                if (asset.uri) {
                  navigation.navigate('Analysis', { 
                    mediaUri: asset.uri, 
                    mediaType: 'photo' 
                  });
                }
              }
            },
          ]
        );
      }
    });
  }, [navigation]);

  const handleRecordVideo = useCallback(() => {
    const options = {
      mediaType: 'video' as MediaType,
      quality: 1,
      durationLimit: 30, // 30 seconds max
    };

    launchCamera(options, (response) => {
      if (response.assets && response.assets[0]) {
        const asset = response.assets[0];
        setSelectedMedia(asset.uri || null);
        setMediaType('video');
        
        Alert.alert(
          'Video Recorded',
          'Would you like to analyze this video?',
          [
            { text: 'Cancel', style: 'cancel' },
            { 
              text: 'Analyze', 
              onPress: () => {
                if (asset.uri) {
                  navigation.navigate('Analysis', { 
                    mediaUri: asset.uri, 
                    mediaType: 'video' 
                  });
                }
              }
            },
          ]
        );
      }
    });
  }, [navigation]);

  const handleSelectFromGallery = useCallback(() => {
    Alert.alert(
      'Select Media Type',
      'What type of media would you like to select?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Photo', onPress: () => selectPhoto() },
        { text: 'Video', onPress: () => selectVideo() },
      ]
    );
  }, []);

  const selectPhoto = () => {
    const options = {
      mediaType: 'photo' as MediaType,
      quality: 1,
    };

    launchImageLibrary(options, (response) => {
      if (response.assets && response.assets[0]) {
        const asset = response.assets[0];
        setSelectedMedia(asset.uri || null);
        setMediaType('photo');
        
        if (asset.uri) {
          navigation.navigate('Analysis', { 
            mediaUri: asset.uri, 
            mediaType: 'photo' 
          });
        }
      }
    });
  };

  const selectVideo = () => {
    const options = {
      mediaType: 'video' as MediaType,
      quality: 1,
    };

    launchImageLibrary(options, (response) => {
      if (response.assets && response.assets[0]) {
        const asset = response.assets[0];
        setSelectedMedia(asset.uri || null);
        setMediaType('video');
        
        if (asset.uri) {
          navigation.navigate('Analysis', { 
            mediaUri: asset.uri, 
            mediaType: 'video' 
          });
        }
      }
    });
  };

  const handleSelectFile = useCallback(async () => {
    try {
      const result = await DocumentPicker.pick({
        type: [DocumentPicker.types.images, DocumentPicker.types.video],
        allowMultiSelection: false,
      });

      if (result && result[0]) {
        const file = result[0];
        const isVideo = file.type?.startsWith('video/');
        
        setSelectedMedia(file.uri);
        setMediaType(isVideo ? 'video' : 'photo');
        
        navigation.navigate('Analysis', { 
          mediaUri: file.uri, 
          mediaType: isVideo ? 'video' : 'photo' 
        });
      }
    } catch (error) {
      if (!DocumentPicker.isCancel(error)) {
        Alert.alert('Error', 'Failed to select file');
      }
    }
  }, [navigation]);

  const captureOptions = [
    {
      title: t('takePhoto'),
      subtitle: 'Capture a microscopy image',
      icon: 'camera-alt',
      color: colors.primary,
      onPress: handleTakePhoto,
    },
    {
      title: t('recordVideo'),
      subtitle: 'Record sperm movement video',
      icon: 'videocam',
      color: colors.secondary,
      onPress: handleRecordVideo,
    },
    {
      title: t('selectFromGallery'),
      subtitle: 'Choose existing media',
      icon: 'photo-library',
      color: colors.accent,
      onPress: handleSelectFromGallery,
    },
    {
      title: 'Select File',
      subtitle: 'Browse device files',
      icon: 'folder-open',
      color: colors.info,
      onPress: handleSelectFile,
    },
  ];

  const tips = [
    {
      icon: 'lightbulb',
      text: 'Ensure good lighting for better detection accuracy',
    },
    {
      icon: 'center-focus-strong',
      text: 'Keep the sample in focus throughout recording',
    },
    {
      icon: 'timer',
      text: 'Record for 10-30 seconds for optimal analysis',
    },
    {
      icon: 'straighten',
      text: 'Hold the device steady during capture',
    },
  ];

  return (
    <View style={styles.container}>
      {/* Header */}
      <Surface style={styles.header}>
        <Text style={styles.headerTitle}>📸 Media Capture</Text>
        <Text style={styles.headerSubtitle}>
          Capture or select media for sperm analysis
        </Text>
      </Surface>

      {/* Capture Options */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Capture Options</Text>
        <View style={styles.optionsGrid}>
          {captureOptions.map((option, index) => (
            <TouchableOpacity
              key={index}
              style={styles.optionCard}
              onPress={option.onPress}
              activeOpacity={0.7}
            >
              <Card style={[styles.optionCardInner, { borderColor: option.color }]}>
                <Card.Content style={styles.optionContent}>
                  <View style={[styles.optionIcon, { backgroundColor: option.color }]}>
                    <Icon name={option.icon} size={32} color="white" />
                  </View>
                  <Text style={styles.optionTitle}>{option.title}</Text>
                  <Text style={styles.optionSubtitle}>{option.subtitle}</Text>
                </Card.Content>
              </Card>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {/* Tips */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>💡 Capture Tips</Text>
        <Card style={styles.tipsCard}>
          <Card.Content>
            {tips.map((tip, index) => (
              <View key={index} style={styles.tipItem}>
                <Icon name={tip.icon} size={20} color={colors.primary} />
                <Text style={styles.tipText}>{tip.text}</Text>
              </View>
            ))}
          </Card.Content>
        </Card>
      </View>

      {/* Recording Status */}
      {isRecording && (
        <Surface style={styles.recordingStatus}>
          <ActivityIndicator size="small" color={colors.error} />
          <Text style={styles.recordingText}>Recording...</Text>
        </Surface>
      )}
    </View>
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
  optionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.md,
  },
  optionCard: {
    width: (width - spacing.lg * 2 - spacing.md) / 2,
  },
  optionCardInner: {
    borderWidth: 2,
    borderRadius: 16,
    ...shadows.small,
  },
  optionContent: {
    alignItems: 'center',
    paddingVertical: spacing.lg,
  },
  optionIcon: {
    width: 64,
    height: 64,
    borderRadius: 32,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.md,
  },
  optionTitle: {
    ...typography.body1,
    fontWeight: '600',
    textAlign: 'center',
    marginBottom: spacing.xs,
  },
  optionSubtitle: {
    ...typography.caption,
    color: colors.textSecondary,
    textAlign: 'center',
  },
  tipsCard: {
    ...shadows.small,
  },
  tipItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.sm,
  },
  tipText: {
    ...typography.body2,
    color: colors.text,
    marginLeft: spacing.md,
    flex: 1,
  },
  recordingStatus: {
    position: 'absolute',
    top: 100,
    left: spacing.lg,
    right: spacing.lg,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: spacing.md,
    borderRadius: 8,
    backgroundColor: colors.error,
  },
  recordingText: {
    ...typography.body1,
    color: 'white',
    marginLeft: spacing.sm,
    fontWeight: '600',
  },
});

export default CameraScreen;
