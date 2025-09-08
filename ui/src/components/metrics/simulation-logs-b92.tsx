"use client"
import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { AlertTriangle, Info, Search, BookOpen, GitBranch, Network, ChevronDown, Activity } from "lucide-react"
import B92WebSocketService, { B92LogEntry } from "@/services/socket-b92"
import { Input } from "../ui/input"
import { DropdownMenu, DropdownMenuCheckboxItem, DropdownMenuContent, DropdownMenuTrigger } from "../ui/dropdown-menu"

const animationStyles = `
  @keyframes slideInFromTop {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .log-entry {
    animation: slideInFromTop 0.3s ease-out;
  }
`

export enum LogLevel {
  DEBUG = "debug",
  INFO = "info",
  WARNING = "warning",
  ERROR = "error",
  CRITICAL = "critical",
  PROTOCOL = "protocol",
  STORY = "story",
  NETWORK = "network"
}

export interface LogI {
  level: LogLevel
  time: string
  source: string
  message: string
}

interface SourceActivity {
  source: string
  lastSeen: number
  count: number
}

const LogLevelColors = {
  [LogLevel.DEBUG]: "bg-gray-100 text-gray-800",
  [LogLevel.INFO]: "bg-blue-100 text-blue-800",
  [LogLevel.WARNING]: "bg-yellow-100 text-yellow-800",
  [LogLevel.ERROR]: "bg-red-100 text-red-800",
  [LogLevel.CRITICAL]: "bg-red-200 text-red-900",
  [LogLevel.PROTOCOL]: "bg-purple-100 text-purple-800",
  [LogLevel.STORY]: "bg-green-100 text-green-800",
  [LogLevel.NETWORK]: "bg-indigo-100 text-indigo-800"
}

const LogLevelIcons = {
  [LogLevel.DEBUG]: Info,
  [LogLevel.INFO]: Info,
  [LogLevel.WARNING]: AlertTriangle,
  [LogLevel.ERROR]: AlertTriangle,
  [LogLevel.CRITICAL]: AlertTriangle,
  [LogLevel.PROTOCOL]: GitBranch,
  [LogLevel.STORY]: BookOpen,
  [LogLevel.NETWORK]: Network
}

export default function SimulationLogsB92() {
  const b92Socket = B92WebSocketService.getInstance()
  const [logFilter, setLogFilter] = useState<LogLevel[]>([LogLevel.STORY, LogLevel.PROTOCOL, LogLevel.ERROR])
  const [searchQuery, setSearchQuery] = useState("")
  
  const [simulationLogs, setSimulationLogs] = useState<LogI[]>([])
  const [filteredLogs, setFilteredLogs] = useState<LogI[]>(simulationLogs)
  const [recentLogIds, setRecentLogIds] = useState<Set<string>>(new Set())
  const [recentActivity, setRecentActivity] = useState<SourceActivity[]>([])

  useEffect(() => {
    // Initialize with existing B92 logs
    const existingLogs = b92Socket.getB92Logs().map(log => ({
      level: log.level as LogLevel,
      time: log.time,
      source: log.source,
      message: log.message
    }))
    setSimulationLogs(existingLogs)
    setFilteredLogs(existingLogs)

    // Add listener for new B92 logs
    const handleNewLog = (log: B92LogEntry) => {
      const newLog: LogI = {
        level: log.level as LogLevel,
        time: log.time,
        source: log.source,
        message: log.message
      }

      setSimulationLogs((prevLogs) => {
        const newLogs = [newLog, ...prevLogs]
        return newLogs
      })

      // Update recent activity tracker
      setRecentActivity((prevActivity) => {
        const now = Date.now()
        const newActivity: SourceActivity = {
          source: newLog.source,
          lastSeen: now,
          count: 1
        }

        const existingIndex = prevActivity.findIndex(a => a.source === newLog.source)
        if (existingIndex >= 0) {
          prevActivity[existingIndex].lastSeen = now
          prevActivity[existingIndex].count += 1
        } else {
          prevActivity.push(newActivity)
        }

        return prevActivity.sort((a, b) => b.lastSeen - a.lastSeen).slice(0, 10)
      })

      // Create unique ID for this log entry
      const logId = `${newLog.time}-${newLog.source}-${Date.now()}`
      setRecentLogIds((prevIds) => {
        const newIds = new Set(prevIds)
        newIds.add(logId)
        return newIds
      })
    }

    b92Socket.addLogListener(handleNewLog)

    return () => {
      b92Socket.removeLogListener(handleNewLog)
    }
  }, [b92Socket])

  useEffect(() => {
    let filtered = simulationLogs

    // Apply log level filter
    if (logFilter.length > 0) {
      filtered = filtered.filter(log => logFilter.includes(log.level))
    }

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(log => 
        log.message.toLowerCase().includes(query) ||
        log.source.toLowerCase().includes(query) ||
        log.level.toLowerCase().includes(query)
      )
    }

    setFilteredLogs(filtered)
  }, [simulationLogs, logFilter, searchQuery])

  const toggleLogLevel = (level: LogLevel) => {
    setLogFilter(prev => 
      prev.includes(level) 
        ? prev.filter(l => l !== level)
        : [...prev, level]
    )
  }

  const clearLogs = () => {
    setSimulationLogs([])
    setFilteredLogs([])
    setRecentLogIds(new Set())
    setRecentActivity([])
    b92Socket.clearB92Logs()
  }

  const getLogLevelCount = (level: LogLevel) => {
    return simulationLogs.filter(log => log.level === level).length
  }

  const getTotalLogs = () => {
    return simulationLogs.length
  }

  return (
    <div className="flex flex-col h-full bg-white border rounded-lg shadow-sm">
      <style>{animationStyles}</style>
      
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b bg-gray-50">
        <div className="flex items-center space-x-2">
          <Activity className="h-5 w-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900">B92 Simulation Logs</h3>
          <Badge variant="secondary" className="bg-blue-100 text-blue-800">
            {getTotalLogs()} logs
          </Badge>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={clearLogs}
            className="text-red-600 hover:text-red-700"
          >
            Clear Logs
          </Button>
        </div>
      </div>

      {/* Filters */}
      <div className="p-4 border-b bg-gray-50">
        <div className="flex items-center space-x-4">
          {/* Search */}
          <div className="flex-1 max-w-md">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search logs..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>

          {/* Log Level Filter */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm">
                <ChevronDown className="h-4 w-4 mr-2" />
                Log Levels ({logFilter.length})
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              {Object.values(LogLevel).map((level) => {
                const Icon = LogLevelIcons[level]
                const count = getLogLevelCount(level)
                return (
                  <DropdownMenuCheckboxItem
                    key={level}
                    checked={logFilter.includes(level)}
                    onCheckedChange={() => toggleLogLevel(level)}
                  >
                    <Icon className="h-4 w-4 mr-2" />
                    {level.toUpperCase()} ({count})
                  </DropdownMenuCheckboxItem>
                )
              })}
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      {/* Recent Activity */}
      {recentActivity.length > 0 && (
        <div className="p-4 border-b bg-blue-50">
          <h4 className="text-sm font-medium text-blue-900 mb-2">Recent Activity</h4>
          <div className="flex flex-wrap gap-2">
            {recentActivity.slice(0, 5).map((activity) => (
              <Badge key={activity.source} variant="outline" className="text-blue-700">
                {activity.source} ({activity.count})
              </Badge>
            ))}
          </div>
        </div>
      )}

      {/* Logs */}
      <div className="flex-1 overflow-auto p-4">
        {filteredLogs.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            <Activity className="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <p>No B92 logs to display</p>
            <p className="text-sm">Start the B92 simulation to see logs here</p>
          </div>
        ) : (
          <div className="space-y-2">
            {filteredLogs.map((log, index) => {
              const Icon = LogLevelIcons[log.level]
              const colorClass = LogLevelColors[log.level]
              
              return (
                <div
                  key={`${log.time}-${log.source}-${index}`}
                  className={`log-entry flex items-start space-x-3 p-3 rounded-lg border bg-white hover:bg-gray-50 transition-colors`}
                >
                  <div className="flex-shrink-0">
                    <Badge className={colorClass}>
                      <Icon className="h-3 w-3 mr-1" />
                      {log.level.toUpperCase()}
                    </Badge>
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="text-sm font-medium text-gray-900">{log.source}</span>
                      <span className="text-xs text-gray-500">{log.time}</span>
                    </div>
                    <p className="text-sm text-gray-700 break-words">{log.message}</p>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
