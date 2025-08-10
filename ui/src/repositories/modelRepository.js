import axios from "./axios";

export default {
    async getModelResponse(userInput, modelName, systemMessage, temperature, maxTokens, topP, topK) {
        try {
            const res = await axios.post(`slm-answer`, {
                userInput: userInput,
                modelName: modelName,
                systemMessage: systemMessage,
                temperature: temperature,
                maxTokens: maxTokens,
                topP: topP,
                topK: topK
            });

            return res;
        } catch (error) {
            console.error("Error getting model response:", error)
            throw error
        }
    }
    ,
    // async getModelResponse() {
    //     try {
    //         const res = await axios.get(`slm-answer`);

    //         return res;
    //     } catch (error) {
    //         console.error("Error getting model response:", error)
    //         throw error
    //     }
    // },
//     async editPolicy(id, name, description, is_active) {
//         try {
//             const res = await axios.post(`policy/edit`, {
//                 id: id,
//                 name: name,
//                 description: description,
//                 is_active: is_active
//             });

//             return res;
//         } catch (error) {
//             console.error("Error editing policy:", error)
//             throw error
//         }
//     },
//     async deletePolicy(id) {
//         try {
//             const res = await axios.delete(`policy/delete/${id}`);

//             return res;
//         } catch (error) {
//             console.error("Error deleting policy:", error)
//             throw error
//         }
//     },
}