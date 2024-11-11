const axios = require('axios');

module.exports = function(RED) {
    function AIQueryNode(config) {
        RED.nodes.createNode(this, config);
        const node = this;
        
        node.on('input', async function(msg) {
            try {
                const response = await axios.post('http://localhost:3000/ai-query', {
                    question: msg.payload.question
                });
                
                msg.payload = response.data;
                node.send(msg);
            } catch(error) {
                node.error(error);
                msg.payload = { status: 'error', error: error.message };
                node.send(msg);
            }
        });
    }
    
    RED.nodes.registerType("ai-query", AIQueryNode);
}