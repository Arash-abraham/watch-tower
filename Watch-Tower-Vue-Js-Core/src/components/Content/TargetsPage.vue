<!-- components/TargetsPage.vue -->
<template>
  <div class="min-h-screen bg-black relative overflow-hidden">
    <!-- Cyberpunk Background Effects -->
    <div class="absolute inset-0 opacity-30">
      <div class="absolute top-2 left-0 w-full h-full bg-[linear-gradient(rgba(0,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px]"></div>
    </div>

    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-[20%] left-[15%] w-1 h-1 bg-cyan-400/40 rounded-full animate-float1"></div>
      <div class="absolute top-[60%] left-[85%] w-1.5 h-1.5 bg-blue-400/30 rounded-full animate-float2"></div>
      <div class="absolute top-[80%] left-[25%] w-1 h-1 bg-cyan-300/40 rounded-full animate-float3"></div>
      <div class="absolute top-[40%] left-[75%] w-0.5 h-0.5 bg-white/30 rounded-full animate-float4"></div>
    </div>

    <!-- Scan Lines -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-cyan-500/30 to-transparent animate-scanX"></div>
      <div class="absolute top-0 left-0 w-[2px] h-full bg-gradient-to-b from-transparent via-cyan-500/30 to-transparent animate-scanY"></div>
    </div>

    <!-- Main Content -->
    <div class="relative z-10 container mx-auto px-4 md:px-6 py-8">
      
      <!-- Header -->
      <div class="mb-8">
        <div class="inline-flex items-center gap-3 px-4 py-2 border border-cyan-500/20 bg-cyan-500/5 backdrop-blur-sm rounded-full mt-10 mb-6">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
          </span>
          <span class="text-cyan-400/70 text-[10px] tracking-[0.2em] font-mono">TARGET INTELLIGENCE</span>
        </div>

        <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
          <div>
            <h1 class="text-3xl md:text-4xl font-black tracking-tight">
              <span class="bg-gradient-to-r from-cyan-400 via-teal-400 to-cyan-400 bg-clip-text text-transparent">
                Attack Surface
              </span>
            </h1>
            <p class="text-gray-500 text-sm mt-2 font-mono">Monitoring {{ totalTargets }} active targets across {{ programs.length }} programs</p>
          </div>

          <!-- Stats Cards -->
          <div class="grid grid-cols-3 gap-3">
            <div class="px-4 py-2 border border-cyan-500/20 bg-black/40 backdrop-blur-sm rounded-lg">
              <div class="text-[10px] text-cyan-400/60 font-mono tracking-wider">IN-SCOPE</div>
              <div class="text-2xl font-bold text-cyan-400">{{ totalInScope }}</div>
            </div>
            <div class="px-4 py-2 border border-cyan-500/20 bg-black/40 backdrop-blur-sm rounded-lg">
              <div class="text-[10px] text-cyan-400/60 font-mono tracking-wider">OUT OF SCOPE</div>
              <div class="text-2xl font-bold text-red-400">{{ totalOutOfScope }}</div>
            </div>
            <div class="px-4 py-2 border border-cyan-500/20 bg-black/40 backdrop-blur-sm rounded-lg">
              <div class="text-[10px] text-cyan-400/60 font-mono tracking-wider">MAX BOUNTY</div>
              <div class="text-2xl font-bold text-amber-400">${{ maxBounty }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters Bar -->
      <div class="flex flex-col md:flex-row justify-between items-center gap-4 mb-8 p-4 border border-cyan-500/10 bg-black/30 backdrop-blur-sm rounded-xl">
        <div class="relative w-full md:w-80">
          <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
            <svg class="w-4 h-4 text-cyan-500/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Search targets by domain or program..."
            class="w-full pl-9 pr-4 py-2 bg-black/50 border border-cyan-500/30 rounded-lg focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 text-white placeholder-gray-500 text-sm font-mono"
          >
        </div>
        
        <div class="flex items-center gap-3 flex-wrap">
          <div class="flex bg-black/50 rounded-lg p-1 border border-cyan-500/20">
            <button 
              v-for="filter in filters" 
              :key="filter.value"
              @click="activeFilter = filter.value; currentPage = 1"
              :class="[
                'px-3 py-1.5 text-xs font-mono rounded-md transition-all',
                activeFilter === filter.value 
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-black font-bold' 
                  : 'text-cyan-400/70 hover:text-cyan-400 hover:bg-cyan-500/10'
              ]"
            >
              {{ filter.label }}
            </button>
          </div>
          
          <div class="flex bg-black/50 rounded-lg p-1 border border-cyan-500/20">
            <button 
              @click="viewMode = 'grid'"
              :class="[
                'p-1.5 rounded-md transition-all',
                viewMode === 'grid' ? 'bg-cyan-500/20 text-cyan-400' : 'text-gray-500 hover:text-cyan-400'
              ]"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
              </svg>
            </button>
            <button 
              @click="viewMode = 'list'"
              :class="[
                'p-1.5 rounded-md transition-all',
                viewMode === 'list' ? 'bg-cyan-500/20 text-cyan-400' : 'text-gray-500 hover:text-cyan-400'
              ]"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Grid View -->
      <div v-if="viewMode === 'grid'" class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-5">
        <div 
          v-for="program in paginatedPrograms" 
          :key="program.name"
          class="group border border-cyan-500/20 bg-black/40 backdrop-blur-sm rounded-xl hover:border-cyan-500/60 transition-all duration-300 hover:transform hover:-translate-y-1 hover:shadow-xl hover:shadow-cyan-500/10"
        >
          <!-- Program Header -->
          <div class="p-5 border-b border-cyan-500/10">
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h3 class="text-lg font-bold text-white group-hover:text-cyan-400 transition-colors">
                  {{ program.name }}
                </h3>
                <div class="flex items-center gap-2 mt-2">
                  <span class="text-[10px] px-2 py-0.5 bg-amber-500/10 text-amber-400 rounded-full font-mono">
                    Max: ${{ program.max_payout.toLocaleString() }}
                  </span>
                  <span v-if="program.managed_by_bugcrowd === 'true'" class="text-[10px] px-2 py-0.5 bg-cyan-500/10 text-cyan-400 rounded-full font-mono">
                    Managed
                  </span>
                </div>
              </div>
              <a 
                :href="program.url" 
                target="_blank"
                class="px-3 py-1.5 text-xs border border-cyan-500/30 text-cyan-400 rounded-lg hover:bg-cyan-500/10 transition-all"
              >
                View
              </a>
            </div>
          </div>

          <!-- In-Scope Targets -->
          <div class="p-5">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <div class="w-2 h-2 bg-emerald-500 rounded-full"></div>
                <span class="text-xs font-mono text-cyan-400/70 tracking-wider">IN-SCOPE TARGETS</span>
              </div>
              <span class="text-[10px] text-gray-500 font-mono">{{ program.targets.in_scope.length }} assets</span>
            </div>
            <div class="space-y-2 max-h-52 overflow-y-auto custom-scrollbar pr-1">
              <div 
                v-for="target in program.targets.in_scope" 
                :key="target.target"
                class="flex items-center justify-between p-2 bg-cyan-500/5 rounded-lg hover:bg-cyan-500/10 transition-all group/target"
              >
                <div class="flex items-center gap-2 flex-1 min-w-0">
                  <div class="w-1.5 h-1.5 bg-emerald-500 rounded-full flex-shrink-0"></div>
                  <div class="text-sm text-gray-300 truncate font-mono">{{ target.target }}</div>
                </div>
                <div class="flex items-center gap-2 flex-shrink-0">
                  <span class="text-[9px] px-1.5 py-0.5 bg-cyan-500/10 rounded text-cyan-400 font-mono uppercase">
                    {{ target.type || 'web' }}
                  </span>
                  <button 
                    @click="copyToClipboard(target.target)"
                    class="opacity-0 group-hover/target:opacity-100 transition-opacity p-1 hover:bg-cyan-500/20 rounded"
                  >
                    <svg class="w-3 h-3 text-gray-500 hover:text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                    </svg>
                  </button>
                </div>
              </div>
              <div v-if="program.targets.in_scope.length === 0" class="text-center text-sm text-gray-600 py-4 italic">
                No targets in scope
              </div>
            </div>
          </div>

          <!-- Out-of-Scope Toggle -->
          <div class="px-5 pb-5" v-if="program.targets.out_of_scope.length > 0">
            <button 
              @click="toggleOutOfScope(program.name)"
              class="flex items-center justify-between w-full text-xs font-mono text-gray-500 hover:text-cyan-400 transition-colors py-1"
            >
              <span>Out-of-Scope ({{ program.targets.out_of_scope.length }})</span>
              <svg class="w-3.5 h-3.5 transition-transform duration-200" :class="{ 'rotate-180': expandedOutOfScope[program.name] }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>
            <div v-show="expandedOutOfScope[program.name]" class="mt-2 space-y-1 max-h-40 overflow-y-auto custom-scrollbar">
              <div 
                v-for="target in program.targets.out_of_scope" 
                :key="target.target"
                class="flex items-center gap-2 text-xs p-1.5 text-gray-600 font-mono"
              >
                <div class="w-1 h-1 bg-red-500/50 rounded-full"></div>
                <span class="truncate">{{ target.target }}</span>
              </div>
            </div>
          </div>

          <!-- Footer Stats -->
          <div class="px-5 py-3 border-t border-cyan-500/10 flex justify-between items-center text-[10px] font-mono">
            <div class="flex gap-3">
              <span class="text-gray-500">API: {{ countType(program.targets.in_scope, 'api') }}</span>
              <span class="text-gray-500">Web: {{ countType(program.targets.in_scope, 'website') }}</span>
            </div>
            <div class="text-cyan-400/50">
              {{ scopeCoverage(program) }}% coverage
            </div>
          </div>
        </div>
      </div>

      <!-- List View -->
      <div v-else class="space-y-3">
        <div 
          v-for="program in paginatedPrograms" 
          :key="program.name"
          class="border border-cyan-500/20 bg-black/40 backdrop-blur-sm rounded-xl hover:border-cyan-500/40 transition-all p-4"
        >
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div class="flex-1">
              <div class="flex items-center gap-3 flex-wrap">
                <h3 class="text-base font-bold text-white">{{ program.name }}</h3>
                <span class="text-[10px] px-2 py-0.5 bg-amber-500/10 text-amber-400 rounded-full font-mono">
                  ${{ program.max_payout.toLocaleString() }}
                </span>
                <span v-if="program.managed_by_bugcrowd === 'true'" class="text-[10px] px-2 py-0.5 bg-cyan-500/10 text-cyan-400 rounded-full font-mono">
                  Managed
                </span>
              </div>
              <div class="flex flex-wrap gap-3 mt-2 text-[11px] font-mono text-gray-500">
                <span>In-Scope: {{ program.targets.in_scope.length }}</span>
                <span>Out-of-Scope: {{ program.targets.out_of_scope.length }}</span>
                <span v-if="program.allows_disclosure === 'true'" class="text-cyan-400">Disclosure Allowed</span>
              </div>
              <div class="flex flex-wrap gap-2 mt-2">
                <span 
                  v-for="target in program.targets.in_scope.slice(0, 4)" 
                  :key="target.target"
                  class="text-[11px] text-gray-400 bg-cyan-500/5 px-2 py-0.5 rounded font-mono"
                >
                  {{ target.target }}
                </span>
                <span v-if="program.targets.in_scope.length > 4" class="text-[11px] text-gray-600">
                  +{{ program.targets.in_scope.length - 4 }}
                </span>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <button 
                @click="copyToClipboard(program.url)"
                class="p-2 rounded-lg hover:bg-cyan-500/10 transition-colors"
              >
                <svg class="w-4 h-4 text-gray-500 hover:text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                </svg>
              </button>
              <a 
                :href="program.url" 
                target="_blank"
                class="px-4 py-1.5 text-sm border border-cyan-500/30 text-cyan-400 rounded-lg hover:bg-cyan-500/10 transition-all"
              >
                View Program
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="filteredPrograms.length > 0" class="flex justify-center items-center gap-3 mt-10 pt-6 border-t border-cyan-500/10">
        <button 
          @click="currentPage--"
          :disabled="currentPage === 1"
          :class="[
            'p-2 rounded-lg transition-all',
            currentPage === 1 ? 'text-gray-600 cursor-not-allowed' : 'text-cyan-400 hover:text-white hover:bg-cyan-500/10'
          ]"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <div class="flex gap-1">
          <button 
            v-for="page in totalPages"
            :key="page"
            @click="currentPage = page"
            :class="[
              'w-8 h-8 text-sm font-mono rounded-lg transition-all',
              currentPage === page 
                ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-black font-bold' 
                : 'text-cyan-400/70 hover:text-white hover:bg-cyan-500/10'
            ]"
          >
            {{ page }}
          </button>
        </div>
        <button 
          @click="currentPage++"
          :disabled="currentPage === totalPages"
          :class="[
            'p-2 rounded-lg transition-all',
            currentPage === totalPages ? 'text-gray-600 cursor-not-allowed' : 'text-cyan-400 hover:text-white hover:bg-cyan-500/10'
          ]"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <!-- Empty State -->
      <div v-if="filteredPrograms.length === 0" class="text-center py-20">
        <div class="w-20 h-20 mx-auto mb-6 border border-cyan-500/20 rounded-2xl flex items-center justify-center bg-black/40">
          <svg class="w-10 h-10 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
        <h3 class="text-xl font-bold text-gray-400 mb-2 font-mono">No targets found</h3>
        <p class="text-gray-600 text-sm">Try adjusting your search or filter criteria</p>
        <button 
          @click="searchQuery = ''; activeFilter = 'all'"
          class="mt-6 px-5 py-2 border border-cyan-500/30 text-cyan-400 rounded-lg hover:bg-cyan-500/10 transition-all text-sm font-mono"
        >
          Clear filters
        </button>
      </div>
    </div>

    <!-- Copy Notification -->
    <div v-if="notification.show" class="fixed bottom-5 right-5 z-50 animate-fade-in">
      <div class="px-4 py-2 rounded-lg bg-gradient-to-r from-cyan-500/20 to-blue-600/20 border border-cyan-500/30 backdrop-blur-md">
        <span class="text-sm text-cyan-400 font-mono">{{ notification.message }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TargetsPage',
  data() {
    return {
      searchQuery: '',
      activeFilter: 'all',
      viewMode: 'grid',
      currentPage: 1,
      itemsPerPage: 6,
      expandedOutOfScope: {},
      notification: { show: false, message: '' },
      filters: [
        { label: 'ALL', value: 'all' },
        { label: 'HIGH BOUNTY', value: 'high' },
        { label: 'MANAGED', value: 'managed' },
        { label: 'DISCLOSURE', value: 'disclosure' }
      ],
      programs: [
        {
          name: "CoinDesk Data - Data API",
          url: "https://bugcrowd.com/engagements/CCData-mbb-og",
          allows_disclosure: "false",
          managed_by_bugcrowd: "true",
          max_payout: 7500,
          targets: {
            in_scope: [
              { type: "api", target: "http://data-api.coindesk.com/" },
              { type: "api", target: "https://tools-api.cryptocompare.com/" }
            ],
            out_of_scope: [
              { type: "website", target: "https://www.coindesk.com/" },
              { type: "website", target: "https://events.coindesk.com" }
            ]
          }
        },
        {
          name: "Acorns Grow, Inc.",
          url: "https://bugcrowd.com/engagements/acorns",
          allows_disclosure: "true",
          managed_by_bugcrowd: "true",
          max_payout: 4000,
          targets: {
            in_scope: [
              { type: "website", target: "https://acorns.com/" },
              { type: "api", target: "https://api.acorns.com/" }
            ],
            out_of_scope: [
              { type: "website", target: "https://help.acorns.com/" }
            ]
          }
        },
        {
          name: "Tesla, Inc.",
          url: "https://bugcrowd.com/engagements/tesla",
          allows_disclosure: "true",
          managed_by_bugcrowd: "false",
          max_payout: 15000,
          targets: {
            in_scope: [
              { type: "website", target: "https://www.tesla.com/" },
              { type: "api", target: "https://owner-api.teslamotors.com/" }
            ],
            out_of_scope: [
              { type: "website", target: "https://shop.tesla.com/" }
            ]
          }
        },
        {
          name: "Microsoft Corporation",
          url: "https://bugcrowd.com/microsoft",
          allows_disclosure: "true",
          managed_by_bugcrowd: "false",
          max_payout: 20000,
          targets: {
            in_scope: [
              { type: "website", target: "https://*.microsoft.com/" },
              { type: "api", target: "https://api.microsoft.com/" }
            ],
            out_of_scope: [
              { type: "website", target: "https://support.microsoft.com/" }
            ]
          }
        },
        {
          name: "Google VRP",
          url: "https://bugcrowd.com/google",
          allows_disclosure: "true",
          managed_by_bugcrowd: "false",
          max_payout: 31337,
          targets: {
            in_scope: [
              { type: "website", target: "https://*.google.com/" },
              { type: "api", target: "https://api.google.com/" }
            ],
            out_of_scope: [
              { type: "website", target: "https://blog.google.com/" }
            ]
          }
        },
        {
          name: "Apple Security Bounty",
          url: "https://bugcrowd.com/apple",
          allows_disclosure: "true",
          managed_by_bugcrowd: "false",
          max_payout: 100000,
          targets: {
            in_scope: [
              { type: "website", target: "https://*.apple.com/" },
              { type: "api", target: "https://api.apple.com/" }
            ],
            out_of_scope: [
              { type: "website", target: "https://support.apple.com/" }
            ]
          }
        }
      ]
    }
  },
  computed: {
    filteredPrograms() {
      let result = this.programs
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(p => 
          p.name.toLowerCase().includes(query) ||
          p.targets.in_scope.some(t => t.target.toLowerCase().includes(query))
        )
      }
      
      if (this.activeFilter === 'high') {
        result = result.filter(p => p.max_payout >= 10000)
      } else if (this.activeFilter === 'managed') {
        result = result.filter(p => p.managed_by_bugcrowd === 'true')
      } else if (this.activeFilter === 'disclosure') {
        result = result.filter(p => p.allows_disclosure === 'true')
      }
      
      return result.sort((a, b) => b.max_payout - a.max_payout)
    },
    paginatedPrograms() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      return this.filteredPrograms.slice(start, start + this.itemsPerPage)
    },
    totalPages() {
      return Math.ceil(this.filteredPrograms.length / this.itemsPerPage)
    },
    totalTargets() {
      return this.programs.reduce((sum, p) => sum + p.targets.in_scope.length, 0)
    },
    totalInScope() {
      return this.programs.reduce((sum, p) => sum + p.targets.in_scope.length, 0)
    },
    totalOutOfScope() {
      return this.programs.reduce((sum, p) => sum + p.targets.out_of_scope.length, 0)
    },
    maxBounty() {
      return Math.max(...this.programs.map(p => p.max_payout)).toLocaleString()
    }
  },
  methods: {
    showNotification(message) {
      this.notification = { show: true, message }
      setTimeout(() => { this.notification.show = false }, 2000)
    },
    scopeCoverage(program) {
      const total = program.targets.in_scope.length + program.targets.out_of_scope.length
      if (total === 0) return 0
      return Math.round((program.targets.in_scope.length / total) * 100)
    },
    countType(targets, type) {
      return targets.filter(t => t.type === type).length
    },
    toggleOutOfScope(programName) {
      this.expandedOutOfScope[programName] = !this.expandedOutOfScope[programName]
    },
    copyToClipboard(text) {
      navigator.clipboard.writeText(text)
      this.showNotification('Copied to clipboard!')
    }
  },
  watch: {
    searchQuery() { this.currentPage = 1 },
    activeFilter() { this.currentPage = 1 }
  },
  mounted() {
    this.programs.forEach(p => {
      this.expandedOutOfScope[p.name] = false
    })
  }
}
</script>

<style scoped>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes scanX {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
@keyframes scanY {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}
@keyframes float1 {
  0%, 100% { transform: translate(0, 0); opacity: 0.3; }
  50% { transform: translate(20px, -20px); opacity: 0.8; }
}
@keyframes float2 {
  0%, 100% { transform: translate(0, 0); opacity: 0.2; }
  50% { transform: translate(-15px, -25px); opacity: 0.7; }
}
@keyframes float3 {
  0%, 100% { transform: translate(0, 0); opacity: 0.4; }
  50% { transform: translate(10px, 20px); opacity: 0.9; }
}
@keyframes float4 {
  0%, 100% { transform: translate(0, 0); opacity: 0.3; }
  50% { transform: translate(-20px, 15px); opacity: 0.8; }
}

.animate-fade-in { animation: fade-in 0.2s ease-out; }
.animate-scanX { animation: scanX 6s linear infinite; }
.animate-scanY { animation: scanY 8s linear infinite; }
.animate-float1 { animation: float1 8s ease-in-out infinite; }
.animate-float2 { animation: float2 10s ease-in-out infinite; }
.animate-float3 { animation: float3 7s ease-in-out infinite; }
.animate-float4 { animation: float4 9s ease-in-out infinite; }

.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: rgba(0, 255, 255, 0.05); border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(0, 255, 255, 0.3); border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(0, 255, 255, 0.5); }
</style>