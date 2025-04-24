import { useEffect, useState } from 'react';
import {
  ChakraProvider,
  Box,
  VStack,
  Heading,
  Text,
  Input,
  Button,
  useToast,
  Container,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Select,
  HStack,
} from '@chakra-ui/react';

interface Resource {
  name: string;
  namespace?: string;
  status?: string;
  [key: string]: any;
}

function App() {
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [command, setCommand] = useState('');
  const [selectedNamespace, setSelectedNamespace] = useState('');
  const [resources, setResources] = useState<{
    namespaces: Resource[];
    pods: Resource[];
    services: Resource[];
    deployments: Resource[];
  }>({
    namespaces: [],
    pods: [],
    services: [],
    deployments: [],
  });
  const toast = useToast();

  // Function to request resources for a specific namespace
  const requestNamespaceResources = (namespace: string) => {
    if (!ws) return;
    ws.send(JSON.stringify({ type: 'get_pods', namespace }));
    ws.send(JSON.stringify({ type: 'get_services', namespace }));
    ws.send(JSON.stringify({ type: 'get_deployments', namespace }));
  };

  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8000/ws/mcp');

    websocket.onopen = () => {
      console.log('Connected to MCP server');
      // Request initial namespaces list
      websocket.send(JSON.stringify({ type: 'get_namespaces' }));
    };

    websocket.onmessage = (event) => {
      const response = JSON.parse(event.data);
      
      if (response.status === 'error') {
        toast({
          title: 'Error',
          description: response.message,
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
        return;
      }

      switch (response.type) {
        case 'namespaces_response':
          setResources(prev => ({ ...prev, namespaces: response.data }));
          break;
        case 'pods_response':
          setResources(prev => ({ ...prev, pods: response.data }));
          break;
        case 'services_response':
          setResources(prev => ({ ...prev, services: response.data }));
          break;
        case 'deployments_response':
          setResources(prev => ({ ...prev, deployments: response.data }));
          break;
        case 'command_response':
          toast({
            title: 'Command executed',
            description: response.data.message,
            status: 'success',
            duration: 5000,
            isClosable: true,
          });
          break;
      }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
      toast({
        title: 'Connection Error',
        description: 'Failed to connect to the server',
        status: 'error',
        duration: null,
        isClosable: true,
      });
    };

    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, []);

  // Effect to request resources when namespace changes
  useEffect(() => {
    if (selectedNamespace) {
      requestNamespaceResources(selectedNamespace);
    }
  }, [selectedNamespace]);

  const handleCommand = () => {
    if (!ws) return;
    ws.send(JSON.stringify({
      type: 'execute_command',
      command,
      namespace: selectedNamespace,
    }));
    setCommand('');
  };

  const ResourceTable = ({ resources, columns }: { resources: Resource[], columns: string[] }) => (
    <Table variant="simple">
      <Thead>
        <Tr>
          {columns.map(col => (
            <Th key={col}>{col}</Th>
          ))}
        </Tr>
      </Thead>
      <Tbody>
        {resources.map((resource, idx) => (
          <Tr key={`${resource.name}-${idx}`}>
            {columns.map(col => (
              <Td key={`${resource.name}-${col}`}>{resource[col.toLowerCase()]}</Td>
            ))}
          </Tr>
        ))}
      </Tbody>
    </Table>
  );

  return (
    <ChakraProvider>
      <Container maxW="container.xl" py={8}>
        <VStack spacing={8} align="stretch">
          <Heading>Kubernetes MCP Dashboard</Heading>
          
          <Box>
            <Text mb={2}>Select Namespace:</Text>
            <Select
              value={selectedNamespace}
              onChange={(e) => setSelectedNamespace(e.target.value)}
              placeholder="Select namespace"
            >
              {resources.namespaces.map((ns) => (
                <option key={ns.name} value={ns.name}>
                  {ns.name}
                </option>
              ))}
            </Select>
          </Box>

          {selectedNamespace && (
            <Box>
              <Text mb={2}>Execute Command:</Text>
              <HStack>
                <Input
                  value={command}
                  onChange={(e) => setCommand(e.target.value)}
                  placeholder="Enter command..."
                  onKeyPress={(e) => e.key === 'Enter' && handleCommand()}
                />
                <Button onClick={handleCommand}>Execute</Button>
              </HStack>
            </Box>
          )}

          {selectedNamespace ? (
            <Tabs>
              <TabList>
                <Tab>Pods</Tab>
                <Tab>Services</Tab>
                <Tab>Deployments</Tab>
              </TabList>

              <TabPanels>
                <TabPanel>
                  <ResourceTable
                    resources={resources.pods.filter(pod => pod.namespace === selectedNamespace)}
                    columns={['Name', 'Status', 'IP', 'Node']}
                  />
                </TabPanel>
                <TabPanel>
                  <ResourceTable
                    resources={resources.services.filter(svc => svc.namespace === selectedNamespace)}
                    columns={['Name', 'Type', 'Cluster IP']}
                  />
                </TabPanel>
                <TabPanel>
                  <ResourceTable
                    resources={resources.deployments.filter(dep => dep.namespace === selectedNamespace)}
                    columns={['Name', 'Replicas', 'Available Replicas']}
                  />
                </TabPanel>
              </TabPanels>
            </Tabs>
          ) : (
            <Box p={4} textAlign="center">
              <Text>Please select a namespace to view resources</Text>
            </Box>
          )}
        </VStack>
      </Container>
    </ChakraProvider>
  );
}

export default App; 