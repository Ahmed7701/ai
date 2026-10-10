# AutoCAD MCP (Model Context Protocol) Plugin

This project integrates AutoCAD with modern AI systems using Model Context Protocol (MCP). It creates a bridge between AutoCAD and AI assistants, allowing AI tools to interact with AutoCAD programmatically.

## Project Architecture

The solution consists of four main projects:

### 1. AutoCadMcp.Model
Contains the core interfaces and models that define the event system:
- `IEvent`: Base interface for all events
- `IEventHandler<TEvent>`: Generic interface for event handlers
- `EventBus`: Central dispatcher that routes events to their handlers
- Event record classes (AlertEvent, AutoLispExecutionEvent, etc.)

### 2. AutoCadMcp.Tcp
Handles communication between the MCP server and the AutoCAD plugin:
- `SocketClient`: Client used by the MCP server to connect to the AutoCAD plugin
- `SocketServer`: TCP server in the AutoCAD plugin that listens for events
- `SocketConfig`: Configuration for the TCP communication
- `EventConverter`: Converts between JSON and event objects

### 3. AutoCADMcpPlugin
The actual AutoCAD plugin that runs within AutoCAD:
- `PluginExtension`: Initializes the plugin when AutoCAD starts
- `McpCommand`: Adds AutoCAD commands to start/stop the MCP server
- Event handlers (AlertEventHandler, AutoLispExecutionHandler, etc.)

### 4. AutoCadMcp
The MCP server that connects to AutoCAD:
- Implements the Model Context Protocol
- Provides tools that can be called by AI assistants
- Forwards requests to AutoCAD through the TCP connection

## Communication Flow

1. AI assistant calls a tool in the MCP server
2. MCP server creates an event object
3. MCP server sends the event via TCP to the AutoCAD plugin
4. AutoCAD plugin receives the event and routes it through the EventBus
5. The appropriate EventHandler processes the event within AutoCAD
6. Response is sent back to the MCP server and ultimately to the AI assistant

## How to Add New Events and Event Handlers

### Step 1: Define a New Event

Create a new record class in the `AutoCadMcp.Model/Event` folder:

```csharp
namespace AutoCadMcp.Model.Event;

public record NewFunctionEvent(string Parameter1, int Parameter2) : IEvent
{
    public string Type => nameof(NewFunctionEvent);
}
```

### Step 2: Create an Event Handler

Add a new handler class in the `AutoCADMcpPlugin/Event` folder.

### Step 3: Add a Tool Method to the MCP Server

Add a method to the `AutoCadMcp/Program.cs` `AutoCadTool` class.

### Step 4: Build and Commit Changes

Run `dotnet build` to verify changes. Keep commits focused and follow the repository's contribution conventions.

## Event Registration

The system automatically discovers and registers events and handlers through reflection in `EventConverter` and `EventBus`.

## Debugging
Use MCP Tool to debug the AutoCAD plugin.

## Best Practices

1. Keep events small and focused on a single operation
2. Use descriptive names for events and handlers
3. Handle exceptions appropriately in handlers
4. Return meaningful response messages
5. Use AutoCAD's ApplicationServices, DatabaseServices, and other APIs as needed in handlers
