export type DetectionResult = {
  type: 'repair' | 'product';
  category: string;
  confidence: number;
  extractedInfo?: {
    budget?: number;
    urgency?: string;
  };
};

// Complete error type labels
export const ERROR_TYPE_LABELS = [
  "GPU Overheat",
  "CPU Overheat",
  "Monitor Issue",
  "No Display / No Signal",
  "Blue Screen (BSOD)",
  "Windows Boot Failure",
  "Slow Performance",
  "Virus / Malware",
  "Driver Issue",
  "SSD Upgrade",
  "RAM Upgrade",
  "GPU Upgrade",
  "PSU / Power Issue",
  "Wi-Fi Adapter Upgrade",
  "OS Reinstall / Corrupted"
] as const;

export type ErrorType = typeof ERROR_TYPE_LABELS[number];

export interface ErrorDetectionResult {
  errorType: string | null;
  confidence: number;
  source: 'rules' | 'nlp' | 'fallback';
  alternatives?: Array<{ label: string; confidence: number }>;
}

/**
 * Priority rule-based error type detector
 * Uses high-priority patterns first, then falls back to generic patterns
 */
export function detectErrorTypeFromText(raw: string): ErrorDetectionResult | null {
  if (!raw || !raw.trim()) {
    return null;
  }

  const text = raw.toLowerCase().trim();
  
  // ============================================
  // HIGH PRIORITY RULES (Specific Patterns)
  // ============================================
  
  // 1. OVERHEAT + GAMING → GPU Overheat (HIGHEST PRIORITY)
  const hasOverheat = /overheat|too hot|high temp|temperature|thermal|heating|hot|fan|cooling/.test(text);
  const hasGaming = /game|gaming|valorant|csgo|pubg|fortnite|fps|apex|league|dota|overwatch|gta|cyberpunk|elden ring|call of duty|cod|fifa|nba|racing/.test(text);
  
  if (hasOverheat && hasGaming) {
    return {
      errorType: "GPU Overheat",
      confidence: 0.9,
      source: 'rules',
      alternatives: [
        { label: "GPU Overheat", confidence: 0.9 },
        { label: "CPU Overheat", confidence: 0.3 }
      ]
    };
  }
  
  // 2. General Overheating → CPU Overheat (if no gaming context)
  if (hasOverheat && !hasGaming) {
    return {
      errorType: "CPU Overheat",
      confidence: 0.8,
      source: 'rules',
      alternatives: [
        { label: "CPU Overheat", confidence: 0.8 },
        { label: "GPU Overheat", confidence: 0.4 }
      ]
    };
  }
  
  // 3. Blue Screen / BSOD
  if (/bsod|blue screen|stop code|0x000000|sad face|error screen|blue screen of death/.test(text)) {
    return {
      errorType: "Blue Screen (BSOD)",
      confidence: 0.9,
      source: 'rules',
      alternatives: [
        { label: "Blue Screen (BSOD)", confidence: 0.9 },
        { label: "Windows Boot Failure", confidence: 0.3 },
        { label: "Driver Issue", confidence: 0.2 }
      ]
    };
  }
  
  // 4. Boot Failure
  if (/no bootable device|boot failure|boot loop|cannot boot|won't boot|not booting|boot error|boot problem/.test(text)) {
    return {
      errorType: "Windows Boot Failure",
      confidence: 0.85,
      source: 'rules',
      alternatives: [
        { label: "Windows Boot Failure", confidence: 0.85 },
        { label: "PSU / Power Issue", confidence: 0.3 }
      ]
    };
  }
  
  // 5. Monitor Power Issues (Check for power-related keywords first)
  const hasPowerKeywords = /not power|won't power|no power|power.*not|power.*off|not turning on|won't turn on|not starting|not booting/.test(text);
  const hasMonitorKeywords = /monitor|display|screen/.test(text);
  
  if (hasMonitorKeywords && hasPowerKeywords) {
    // Monitor won't power on - likely PSU or RAM issue
    return {
      errorType: "PSU / Power Issue",
      confidence: 0.85,
      source: 'rules',
      alternatives: [
        { label: "PSU / Power Issue", confidence: 0.85 },
        { label: "RAM Upgrade", confidence: 0.6 },
        { label: "No Display / No Signal", confidence: 0.5 },
        { label: "Windows Boot Failure", confidence: 0.4 }
      ]
    };
  }
  
  // 6. No Display / No Signal (but monitor has power)
  if (/no signal|no display|black screen|blank screen|monitor.*no.*signal|display.*not.*working|screen.*black|no image|nothing on screen/.test(text) && !hasPowerKeywords) {
    return {
      errorType: "No Display / No Signal",
      confidence: 0.85,
      source: 'rules',
      alternatives: [
        { label: "No Display / No Signal", confidence: 0.85 },
        { label: "Monitor Issue", confidence: 0.6 },
        { label: "GPU Issue", confidence: 0.4 }
      ]
    };
  }
  
  // 7. PC Won't Power On / Not Starting
  if (/won't power|not power|no power|power.*not|won't turn on|not turning on|not starting|not booting|computer.*not.*on|pc.*not.*on/.test(text) && !hasMonitorKeywords) {
    return {
      errorType: "PSU / Power Issue",
      confidence: 0.85,
      source: 'rules',
      alternatives: [
        { label: "PSU / Power Issue", confidence: 0.85 },
        { label: "RAM Upgrade", confidence: 0.5 },
        { label: "Windows Boot Failure", confidence: 0.4 }
      ]
    };
  }
  
  // 8. PC Restarts / Shutdowns
  if (/restart|shutdown|turns off|power off|shuts down|reboot|restarting|keeps restarting/.test(text)) {
    // Check if during gaming
    if (hasGaming) {
      return {
        errorType: "GPU Overheat",
        confidence: 0.8,
        source: 'rules',
        alternatives: [
          { label: "GPU Overheat", confidence: 0.8 },
          { label: "PSU / Power Issue", confidence: 0.5 }
        ]
      };
    }
    return {
      errorType: "PSU / Power Issue",
      confidence: 0.75,
      source: 'rules',
      alternatives: [
        { label: "PSU / Power Issue", confidence: 0.75 },
        { label: "CPU Overheat", confidence: 0.4 },
        { label: "RAM Upgrade", confidence: 0.3 }
      ]
    };
  }
  
  // 9. Upgrade Phrases
  if (/upgrade.*ssd|add.*ssd|bigger.*ssd|more.*ssd|install.*ssd|new.*ssd|1tb.*ssd|2tb.*ssd|500gb.*ssd/.test(text)) {
    return {
      errorType: "SSD Upgrade",
      confidence: 0.9,
      source: 'rules',
      alternatives: [
        { label: "SSD Upgrade", confidence: 0.9 }
      ]
    };
  }
  
  if (/upgrade.*ram|need.*ram|more.*ram|add.*ram|install.*ram|new.*ram|increase.*ram|upgrade.*memory/.test(text)) {
    return {
      errorType: "RAM Upgrade",
      confidence: 0.9,
      source: 'rules',
      alternatives: [
        { label: "RAM Upgrade", confidence: 0.9 }
      ]
    };
  }
  
  if (/upgrade.*gpu|new.*gpu|better.*gpu|graphics.*card|video.*card/.test(text)) {
    return {
      errorType: "GPU Upgrade",
      confidence: 0.85,
      source: 'rules',
      alternatives: [
        { label: "GPU Upgrade", confidence: 0.85 }
      ]
    };
  }
  
  // 10. Slow Performance
  if (/slow|lag|lagging|freeze|freezing|stuck|hanging|unresponsive|not responding|sluggish/.test(text)) {
    return {
      errorType: "Slow Performance",
      confidence: 0.7,
      source: 'rules',
      alternatives: [
        { label: "Slow Performance", confidence: 0.7 },
        { label: "Virus / Malware", confidence: 0.3 },
        { label: "Driver Issue", confidence: 0.2 }
      ]
    };
  }
  
  // 11. Virus / Malware
  if (/virus|malware|infected|trojan|spyware|ransomware|antivirus|security|threat/.test(text)) {
    return {
      errorType: "Virus / Malware",
      confidence: 0.85,
      source: 'rules',
      alternatives: [
        { label: "Virus / Malware", confidence: 0.85 }
      ]
    };
  }
  
  // 12. Driver Issue
  if (/driver|device manager|hardware.*not|peripheral.*not|printer.*not|scanner.*not/.test(text)) {
    return {
      errorType: "Driver Issue",
      confidence: 0.75,
      source: 'rules',
      alternatives: [
        { label: "Driver Issue", confidence: 0.75 }
      ]
    };
  }
  
  // 13. OS Reinstall / Corrupted
  if (/reinstall.*windows|reinstall.*os|corrupted.*windows|windows.*corrupted|format.*pc|fresh.*install|reset.*pc/.test(text)) {
    return {
      errorType: "OS Reinstall / Corrupted",
      confidence: 0.85,
      source: 'rules',
      alternatives: [
        { label: "OS Reinstall / Corrupted", confidence: 0.85 }
      ]
    };
  }
  
  // 14. Wi-Fi Adapter Upgrade
  if (/wifi.*upgrade|wireless.*upgrade|network.*adapter|wifi.*not|internet.*not|connection.*problem/.test(text)) {
    return {
      errorType: "Wi-Fi Adapter Upgrade",
      confidence: 0.75,
      source: 'rules',
      alternatives: [
        { label: "Wi-Fi Adapter Upgrade", confidence: 0.75 }
      ]
    };
  }
  
  // ============================================
  // LOWER PRIORITY RULES (Generic Patterns)
  // ============================================
  
  // RAM Issues (when mentioned with boot/power problems)
  if (/ram|memory/.test(text) && (hasPowerKeywords || /not boot|won't boot|not start/.test(text))) {
    return {
      errorType: "RAM Upgrade",
      confidence: 0.75,
      source: 'rules',
      alternatives: [
        { label: "RAM Upgrade", confidence: 0.75 },
        { label: "PSU / Power Issue", confidence: 0.5 },
        { label: "Windows Boot Failure", confidence: 0.4 }
      ]
    };
  }
  
  // Monitor Issue (lower confidence - only if no power keywords)
  if (/monitor|display|screen/.test(text) && !hasPowerKeywords && !/no signal|no display|black screen/.test(text)) {
    return {
      errorType: "Monitor Issue",
      confidence: 0.6,
      source: 'rules',
      alternatives: [
        { label: "Monitor Issue", confidence: 0.6 },
        { label: "No Display / No Signal", confidence: 0.3 }
      ]
    };
  }
  
  // Generic device fallbacks (LOWEST PRIORITY, LOW CONFIDENCE)
  if (/desktop|pc|computer/.test(text) && !hasOverheat && !hasGaming) {
    return {
      errorType: "General Desktop Issue",
      confidence: 0.4,
      source: 'rules',
      alternatives: []
    };
  }
  
  if (/laptop|notebook/.test(text) && !hasOverheat && !hasGaming) {
    return {
      errorType: "General Laptop Issue",
      confidence: 0.4,
      source: 'rules',
      alternatives: []
    };
  }
  
  // No match found
  return null;
}

// Error type patterns for repair detection (legacy support)
const ERROR_PATTERNS = {
  'GPU Overheat': ['gpu', 'graphics', 'overheat', 'overheating', 'thermal', 'temperature', 'hot', 'fan', 'cooling', 'heating'],
  'Blue Screen (BSOD)': ['blue screen', 'bsod', 'blue screen of death', 'crash', 'freeze', 'hang', 'stopped working', 'error screen'],
  'Boot Failure': ['boot', 'startup', 'won\'t start', 'not starting', 'power on', 'turn on', 'start up', 'booting', 'boot loop'],
  'SSD Upgrade': ['ssd', 'solid state', 'hard drive', 'storage', 'upgrade ssd', 'install ssd', 'new ssd', 'disk space'],
  'RAM Upgrade': ['ram', 'memory', 'upgrade ram', 'install ram', 'add memory', 'more ram', 'new ram', 'ddr'],
  'OS Installation': ['os', 'operating system', 'windows', 'install', 'reinstall', 'format', 'fresh install', 'system'],
  'Laptop Screen Repair': ['screen', 'display', 'lcd', 'led', 'cracked screen', 'broken screen', 'screen repair', 'monitor'],
  'Data Recovery': ['data', 'recovery', 'lost files', 'deleted files', 'backup', 'restore', 'file recovery'],
  'PSU / Power Issue': ['psu', 'power supply', 'power', 'not turning on', 'no power', 'power issue', 'battery'],
  'Wi-Fi Adapter Upgrade': ['wifi', 'wireless', 'network', 'internet', 'adapter', 'connection', 'ethernet'],
  'Motherboard Issue': ['motherboard', 'mainboard', 'mobo', 'board', 'circuit'],
  'Keyboard Repair': ['keyboard', 'keys', 'typing', 'input', 'mechanical keyboard'],
  'Audio Issue': ['sound', 'audio', 'speaker', 'headphone', 'microphone', 'volume'],
  'Driver Issue': ['driver', 'device manager', 'hardware', 'peripheral', 'printer']
};

// Product patterns for product detection
const PRODUCT_PATTERNS = {
  'Laptop': ['laptop', 'notebook', 'macbook', 'ultrabook', 'gaming laptop', 'business laptop'],
  'Desktop': ['desktop', 'pc', 'computer', 'tower', 'workstation', 'gaming pc'],
  'Mouse': ['mouse', 'mice', 'trackball', 'wireless mouse', 'gaming mouse'],
  'Keyboard': ['keyboard', 'mechanical keyboard', 'wireless keyboard', 'gaming keyboard'],
  'Monitor': ['monitor', 'display', 'screen', 'lcd', 'led', '4k monitor', 'gaming monitor'],
  'RAM': ['ram', 'memory', 'ddr4', 'ddr5', 'memory stick', 'memory module', 'memory card', 'random access memory'],
  'SSD': ['ssd', 'solid state drive', 'nvme', 'm.2', 'storage drive', 'solid state'],
  'GPU': ['gpu', 'graphics card', 'graphic card', 'video card', 'nvidia', 'amd', 'rtx', 'gtx', 'graphics', 'graphic'],
  'CPU': ['cpu', 'processor', 'intel', 'amd', 'ryzen', 'core i', 'threadripper'],
  'Motherboard': ['motherboard', 'mainboard', 'mobo', 'mother board', 'main board'],
  'PSU': ['psu', 'power supply', 'power unit', 'smps', 'power supply unit'],
  'Case': ['case', 'chassis', 'tower case', 'pc case', 'computer case'],
  'Cooling': ['cooling', 'fan', 'heatsink', 'cooler', 'liquid cooling', 'air cooler'],
  'Wi-Fi Adapter': ['wifi adapter', 'wireless adapter', 'network adapter', 'wifi card', 'wireless card']
};

// Budget extraction patterns
const BUDGET_PATTERNS = [
  { pattern: /under\s*(\d+)[kK]?/i, multiplier: 1000 },
  { pattern: /below\s*(\d+)[kK]?/i, multiplier: 1000 },
  { pattern: /less\s*than\s*(\d+)[kK]?/i, multiplier: 1000 },
  { pattern: /maximum\s*(\d+)[kK]?/i, multiplier: 1000 },
  { pattern: /budget\s*(\d+)[kK]?/i, multiplier: 1000 },
  { pattern: /(\d+)\s*lkr/i, multiplier: 1 },
  { pattern: /(\d+)\s*rupees/i, multiplier: 1 }
];

// Urgency extraction patterns
const URGENCY_PATTERNS = {
  high: ['urgent', 'asap', 'immediately', 'emergency', 'critical', 'rush', 'fast', 'quick'],
  normal: ['normal', 'standard', 'regular', 'when possible', 'flexible', 'no rush']
};

export function detectQueryType(query: string): DetectionResult {
  const lowerQuery = query.toLowerCase();
  
  // Check for buy/purchase intent first - prioritize product detection
  const hasBuyIntent = lowerQuery.includes('buy') || lowerQuery.includes('purchase') || 
                       lowerQuery.includes('want to buy') || lowerQuery.includes('want a') ||
                       lowerQuery.includes('looking for') || lowerQuery.includes('need to buy');
  
  // Check for product patterns (prioritize if buy intent exists)
  for (const [productType, keywords] of Object.entries(PRODUCT_PATTERNS)) {
    const matches = keywords.filter(keyword => lowerQuery.includes(keyword));
    if (matches.length > 0) {
      // Boost confidence if buy intent is present
      const baseConfidence = matches.length / keywords.length;
      const confidence = hasBuyIntent ? Math.min(1.0, baseConfidence + 0.3) : baseConfidence;
      
      return {
        type: 'product',
        category: productType,
        confidence: confidence,
        extractedInfo: extractAdditionalInfo(lowerQuery)
      };
    }
  }
  
  // If buy intent but no specific product found, still return product type
  if (hasBuyIntent) {
    // Try to extract product from common phrases
    if (lowerQuery.includes('ram') || lowerQuery.includes('memory')) {
      return {
        type: 'product',
        category: 'RAM',
        confidence: 0.7,
        extractedInfo: extractAdditionalInfo(lowerQuery)
      };
    }
    if (lowerQuery.includes('graphic') || lowerQuery.includes('graphics')) {
      return {
        type: 'product',
        category: 'GPU',
        confidence: 0.8,
        extractedInfo: extractAdditionalInfo(lowerQuery)
      };
    }
    if (lowerQuery.includes('ssd') || lowerQuery.includes('storage')) {
      return {
        type: 'product',
        category: 'SSD',
        confidence: 0.7,
        extractedInfo: extractAdditionalInfo(lowerQuery)
      };
    }
    
    return {
      type: 'product',
      category: 'General Product',
      confidence: 0.5,
      extractedInfo: extractAdditionalInfo(lowerQuery)
    };
  }
  
  // Check for error patterns (repair)
  for (const [errorType, keywords] of Object.entries(ERROR_PATTERNS)) {
    const matches = keywords.filter(keyword => lowerQuery.includes(keyword));
    if (matches.length > 0) {
      return {
        type: 'repair',
        category: errorType,
        confidence: matches.length / keywords.length,
        extractedInfo: extractAdditionalInfo(lowerQuery)
      };
    }
  }
  
  // Default fallback
  return {
    type: 'repair',
    category: 'General Repair',
    confidence: 0.1,
    extractedInfo: extractAdditionalInfo(lowerQuery)
  };
}

function extractAdditionalInfo(query: string): DetectionResult['extractedInfo'] {
  const info: DetectionResult['extractedInfo'] = {};
  
  // Extract budget
  for (const { pattern, multiplier } of BUDGET_PATTERNS) {
    const match = query.match(pattern);
    if (match) {
      const amount = parseInt(match[1]) * multiplier;
      if (amount >= 10000 && amount <= 1000000) { // Reasonable range
        info.budget = amount;
        break;
      }
    }
  }
  
  // Extract urgency
  for (const [urgency, keywords] of Object.entries(URGENCY_PATTERNS)) {
    if (keywords.some(keyword => query.includes(keyword))) {
      info.urgency = urgency;
      break;
    }
  }
  
  return Object.keys(info).length > 0 ? info : undefined;
}

export function getMatchReason(recommendation: Record<string, unknown>, queryType: string): string {
  const reasons = [];
  
  if (recommendation.verified === true || recommendation.verified === 1) {
    reasons.push('Verified shop');
  }
  
  if (recommendation.district_match === 1) {
    reasons.push('Same district');
  }
  
  if (recommendation.budget_fit === 1) {
    reasons.push('Budget fit');
  }
  
  if (recommendation.type_match === 1) {
    reasons.push('Specialization match');
  }
  
  if (typeof recommendation.avg_rating === 'number' && recommendation.avg_rating >= 4.0) {
    reasons.push('High rating');
  }
  
  if (recommendation.is_open === true) {
    reasons.push('Open now');
  }
  
  // Add query-specific reasons
  if (queryType === 'repair') {
    if (recommendation.specialization) {
      reasons.push(`${recommendation.specialization} specialist`);
    }
  }
  
  return reasons.length > 0 ? reasons.join(' · ') : 'Recommended based on location and rating';
}
