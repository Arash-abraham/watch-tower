<template>
    <div class="min-h-screen text-white pt-20 px-6">
      <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <div class="mb-8">
          <div class="inline-flex items-center gap-3 px-4 py-2 border border-cyan-500/20 bg-cyan-500/5 backdrop-blur-sm rounded-full">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
            </span>
            <span class="text-cyan-400/70 text-[10px] tracking-[0.2em] font-mono">ALERTS</span>
          </div>
        </div>
  
        <!-- Title -->
        <div class="mb-10">
          <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-2">
            <span class="text-white">Alerts</span>
          </h1>
          <p class="text-gray-500 text-sm">Real-time alert management and notifications</p>
        </div>
  
        <!-- Alert Summary -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
          <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-4">
            <div class="text-gray-500 text-sm">Total Alerts</div>
            <div class="text-2xl font-bold text-white mt-1">47</div>
          </div>
          <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-4">
            <div class="text-gray-500 text-sm">Critical</div>
            <div class="text-2xl font-bold text-red-500 mt-1">3</div>
          </div>
          <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-4">
            <div class="text-gray-500 text-sm">Warning</div>
            <div class="text-2xl font-bold text-yellow-500 mt-1">8</div>
          </div>
          <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-4">
            <div class="text-gray-500 text-sm">Resolved</div>
            <div class="text-2xl font-bold text-green-500 mt-1">36</div>
          </div>
        </div>
  
        <!-- Alert List -->
        <div class="bg-gray-900/50 border border-gray-800 rounded-xl overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-800 flex items-center justify-between">
            <h3 class="text-sm font-medium text-gray-300">Recent Alerts</h3>
            <div class="flex items-center gap-3 text-xs">
              <span class="text-gray-600">Showing latest 10</span>
              <button class="text-cyan-500 hover:text-cyan-400 transition-colors">View All</button>
            </div>
          </div>
          <div class="divide-y divide-gray-800">
            <div v-for="alert in alerts" :key="alert.id" class="px-6 py-4 hover:bg-gray-800/30 transition-colors">
              <div class="flex items-start justify-between">
                <div class="flex items-start gap-4">
                  <div class="w-1.5 h-1.5 rounded-full mt-2" :class="getSeverityClass(alert.severity)"></div>
                  <div>
                    <div class="flex items-center gap-3">
                      <span class="text-sm font-medium text-white">{{ alert.title }}</span>
                      <span class="text-xs px-2 py-0.5 rounded-full" :class="getSeverityBadgeClass(alert.severity)">
                        {{ alert.severity }}
                      </span>
                    </div>
                    <p class="text-sm text-gray-400 mt-1">{{ alert.description }}</p>
                    <div class="flex items-center gap-3 mt-2">
                      <span class="text-xs text-gray-600">{{ alert.source }}</span>
                      <span class="text-xs text-gray-600">•</span>
                      <span class="text-xs text-gray-600">{{ alert.time }}</span>
                    </div>
                  </div>
                </div>
                <span class="text-xs font-mono" :class="getStatusClass(alert.status)">
                  {{ alert.status }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  const alerts = [
    {
      id: 1,
      title: 'Database Connection Failed',
      description: 'Unable to connect to primary database server',
      severity: 'critical',
      source: 'Database Monitor',
      time: '15 minutes ago',
      status: 'active'
    },
    {
      id: 2,
      title: 'High CPU Usage Detected',
      description: 'CPU utilization exceeded 85% on web server',
      severity: 'warning',
      source: 'System Monitor',
      time: '1 hour ago',
      status: 'active'
    },
    {
      id: 3,
      title: 'SSL Certificate Expiring',
      description: 'Certificate for api.example.com expires in 7 days',
      severity: 'warning',
      source: 'Security Monitor',
      time: '3 hours ago',
      status: 'active'
    },
    {
      id: 4,
      title: 'Target Added Successfully',
      description: 'New target configured and is now being monitored',
      severity: 'info',
      source: 'System',
      time: '5 hours ago',
      status: 'resolved'
    },
    {
      id: 5,
      title: 'Ping Monitor Restarted',
      description: 'Ping monitor service was restarted automatically',
      severity: 'info',
      source: 'System',
      time: '8 hours ago',
      status: 'resolved'
    }
  ]
  
  const getSeverityClass = (severity) => {
    return {
      'critical': 'bg-red-500',
      'warning': 'bg-yellow-500',
      'info': 'bg-blue-500'
    }[severity] || 'bg-gray-500'
  }
  
  const getSeverityBadgeClass = (severity) => {
    return {
      'critical': 'bg-red-500/20 text-red-400',
      'warning': 'bg-yellow-500/20 text-yellow-400',
      'info': 'bg-blue-500/20 text-blue-400'
    }[severity] || 'bg-gray-500/20 text-gray-400'
  }
  
  const getStatusClass = (status) => {
    return {
      'active': 'text-red-500/70',
      'resolved': 'text-green-500/70'
    }[status] || 'text-gray-500/70'
  }
  </script>