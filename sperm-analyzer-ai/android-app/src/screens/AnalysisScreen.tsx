/**
 * Analysis Screen - AI processing interface
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  Alert,
  Image,
  Dimensions,
} from 'react-native';
import {
  Text,
  Button,
  Card,
  ProgressBar,
  Surface,
  ActivityIndicator,
} from 'react-native-paper';
import { useTranslation } from 'react-i18next';
import Icon from 'react-native-vector-icons/MaterialIcons';
import Video from 'react-native-video';

import AIProcessor, { AnalysisResult } from '../services/AIProcessor';
import { colors, spacing, typography, shadows } from '../styles/theme';

const { width } = Dimensions.get('window');

interface AnalysisScreenProps {
  route: {
    params: {
      mediaUri: string;
      mediaType: 'photo' | 'video';
    };
  };
  navigation: any;
}

const AnalysisScreen: React.FC<AnalysisScreenProps> = ({ route, navigation }) => {
  const { t } = useTranslation();
  const { mediaUri, mediaType } = route.params;
  
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState('');

  useEffect(() => {
    if (mediaUri) {
      startAnalysis();
    }
  }, [mediaUri]);

  const startAnalysis = async () => {
    setIsAnalyzing(true);
    setProgress(0);
    setError(null);
    setCurrentStep('Initializing AI models...');

    try {
      let result: AnalysisResult;

      if (mediaType === 'photo') {
        setCurrentStep('Analyzing image...');
        result = await AIProcessor.analyzeImage(mediaUri);
      } else {
        setCurrentStep('Processing video frames...');
        result = await AIProcessor.analyzeVideo(mediaUri, (progressValue) => {
          setProgress(progressValue);
          if (progressValue < 0.3) {
            setCurrentStep('Detecting sperm...');
          } else if (progressValue < 0.7) {
            setCurrentStep('Tracking movement...');
          } else if (progressValue < 0.9) {
            setCurrentStep('Calculating CASA metrics...');
          } else {
            setCurrentStep('Finalizing results...');
          }
        });
      }

      setAnalysisResult(result);
      setCurrentStep('Analysis complete!');
      setProgress(1);
      
      // Navigate to results after a short delay
      setTimeout(() => {
        navigation.navigate('Results', { analysisResult: result });
      }, 1500);

    } catch (err) {
      console.error('Analysis error:', err);
      setError(err instanceof Error ? err.message : 'Analysis failed');
      setCurrentStep('Analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const retryAnalysis = () => {
    setError(null);
    startAnalysis();
  };

  const renderMediaPreview = () => {
    if (mediaType === 'photo') {
      return (
        <Image
          source={{ uri: mediaUri }}
          style={styles.mediaPreview}
          resizeMode="contain"
        />
      );
    } else {
      return (
        <Video
          source={{ uri: mediaUri }}
          style={styles.mediaPreview}
          resizeMode="contain"
          repeat
          muted
          paused={!isAnalyzing}
        />
      );
    }
  };

  const renderAnalysisStatus = () => {
    if (error) {
      return (
        <Card style={[styles.statusCard, { borderColor: colors.error }]}>
          <Card.Content style={styles.statusContent}>
            <Icon name="error" size={48} color={colors.error} />
            <Text style={[styles.statusTitle, { color: colors.error }]}>
              Analysis Failed
            </Text>
            <Text style={styles.statusMessage}>{error}</Text>
            <Button
              mode="contained"
              onPress={retryAnalysis}
              style={styles.retryButton}
            >
              Retry Analysis
            </Button>
          </Card.Content>
        </Card>
      );
    }

    if (analysisResult) {
      return (
        <Card style={[styles.statusCard, { borderColor: colors.success }]}>
          <Card.Content style={styles.statusContent}>
            <Icon name="check-circle" size={48} color={colors.success} />
            <Text style={[styles.statusTitle, { color: colors.success }]}>
              Analysis Complete!
            </Text>
            <Text style={styles.statusMessage}>
              Found {analysisResult.sperm_count} sperm
            </Text>
            <Text style={styles.processingTime}>
              Processing time: {(analysisResult.processing_time / 1000).toFixed(1)}s
            </Text>
          </Card.Content>
        </Card>
      );
    }

    return (
      <Card style={styles.statusCard}>
        <Card.Content style={styles.statusContent}>
          <ActivityIndicator size="large" color={colors.primary} />
          <Text style={styles.statusTitle}>
            {mediaType === 'photo' ? t('processingImage') : t('processingVideo')}
          </Text>
          <Text style={styles.currentStep}>{currentStep}</Text>
          
          {mediaType === 'video' && (
            <View style={styles.progressContainer}>
              <ProgressBar
                progress={progress}
                color={colors.primary}
                style={styles.progressBar}
              />
              <Text style={styles.progressText}>
                {Math.round(progress * 100)}%
              </Text>
            </View>
          )}
        </Card.Content>
      </Card>
    );
  };

  const analysisSteps = [
    {
      icon: 'camera-alt',
      title: 'Media Capture',
      description: 'Image/video loaded successfully',
      completed: true,
    },
    {
      icon: 'psychology',
      title: 'AI Detection',
      description: 'YOLOv8 model detecting sperm',
      completed: progress > 0.3 || !!analysisResult,
    },
    {
      icon: 'track-changes',
      title: 'Movement Tracking',
      description: 'DeepSORT tracking sperm paths',
      completed: progress > 0.7 || !!analysisResult,
    },
    {
      icon: 'analytics',
      title: 'CASA Metrics',
      description: 'Calculating velocity parameters',
      completed: !!analysisResult,
    },
  ];

  return (
    <View style={styles.container}>
      {/* Media Preview */}
      <Surface style={styles.previewContainer}>
        {renderMediaPreview()}
        <View style={styles.mediaInfo}>
          <Text style={styles.mediaType}>
            {mediaType === 'photo' ? '📸 Image' : '📹 Video'}
          </Text>
        </View>
      </Surface>

      {/* Analysis Status */}
      <View style={styles.section}>
        {renderAnalysisStatus()}
      </View>

      {/* Analysis Steps */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Analysis Pipeline</Text>
        <Card style={styles.stepsCard}>
          <Card.Content>
            {analysisSteps.map((step, index) => (
              <View key={index} style={styles.stepItem}>
                <View style={[
                  styles.stepIcon,
                  { backgroundColor: step.completed ? colors.success : colors.border }
                ]}>
                  <Icon
                    name={step.completed ? 'check' : step.icon}
                    size={20}
                    color={step.completed ? 'white' : colors.textSecondary}
                  />
                </View>
                <View style={styles.stepContent}>
                  <Text style={[
                    styles.stepTitle,
                    { color: step.completed ? colors.text : colors.textSecondary }
                  ]}>
                    {step.title}
                  </Text>
                  <Text style={styles.stepDescription}>
                    {step.description}
                  </Text>
                </View>
              </View>
            ))}
          </Card.Content>
        </Card>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  previewContainer: {
    margin: spacing.lg,
    borderRadius: 12,
    overflow: 'hidden',
    ...shadows.medium,
  },
  mediaPreview: {
    width: '100%',
    height: 200,
    backgroundColor: colors.surface,
  },
  mediaInfo: {
    position: 'absolute',
    top: spacing.md,
    right: spacing.md,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: 20,
  },
  mediaType: {
    ...typography.caption,
    color: 'white',
    fontWeight: '600',
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
  statusCard: {
    borderWidth: 2,
    borderRadius: 16,
    ...shadows.small,
  },
  statusContent: {
    alignItems: 'center',
    paddingVertical: spacing.lg,
  },
  statusTitle: {
    ...typography.h4,
    textAlign: 'center',
    marginTop: spacing.md,
    marginBottom: spacing.sm,
  },
  statusMessage: {
    ...typography.body1,
    color: colors.textSecondary,
    textAlign: 'center',
    marginBottom: spacing.sm,
  },
  processingTime: {
    ...typography.caption,
    color: colors.textSecondary,
    textAlign: 'center',
  },
  currentStep: {
    ...typography.body2,
    color: colors.primary,
    textAlign: 'center',
    marginTop: spacing.sm,
    fontWeight: '600',
  },
  progressContainer: {
    width: '100%',
    marginTop: spacing.lg,
    alignItems: 'center',
  },
  progressBar: {
    width: '100%',
    height: 8,
    borderRadius: 4,
  },
  progressText: {
    ...typography.caption,
    color: colors.textSecondary,
    marginTop: spacing.sm,
  },
  retryButton: {
    marginTop: spacing.md,
  },
  stepsCard: {
    ...shadows.small,
  },
  stepItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.md,
  },
  stepIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.md,
  },
  stepContent: {
    flex: 1,
  },
  stepTitle: {
    ...typography.body1,
    fontWeight: '600',
    marginBottom: spacing.xs,
  },
  stepDescription: {
    ...typography.caption,
    color: colors.textSecondary,
  },
});

export default AnalysisScreen;
