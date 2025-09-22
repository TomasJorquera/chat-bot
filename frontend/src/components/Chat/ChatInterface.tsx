import React, { useState, useRef, useEffect } from 'react';
import { Send, ArrowLeft, RotateCcw, FileText, Loader } from 'lucide-react';
import { Message } from '../../types';

interface ChatInterfaceProps {
  character: 'Teo' | 'Josefina';
  onBack: () => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ character, onBack }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const characterInfo = {
    Teo: {
      emoji: '🧒',
      age: 9,
      grade: '4º Básico',
      personality: 'Tímido pero curioso, prefiere ejemplos visuales',
      greeting: '¡Hola! Soy Teo. A veces me cuesta leer, pero me gusta aprender con dibujos y colores. ¿Me puedes ayudar?'
    },
    Josefina: {
      emoji: '👧',
      age: 15,
      grade: '1º Medio',
      personality: 'Tímida, aprende mejor con ejemplos concretos',
      greeting: '¡Hola! Soy Josefina. Me gusta la música y el fútbol. A veces necesito que me expliquen las cosas con ejemplos. ¿Podemos conversar?'
    }
  };

  useEffect(() => {
    // Initial greeting
    const greeting: Message = {
      id: Date.now().toString(),
      content: characterInfo[character].greeting,
      sender: 'character',
      timestamp: new Date()
    };
    setMessages([greeting]);
  }, [character]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const simulateCharacterResponse = async (userMessage: string) => {
    setIsTyping(true);
    
    // Simulate thinking time
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
    
    const responses = {
      Teo: [
        '¡Eso es interesante! ¿Me puedes explicar con un ejemplo?',
        'Me gusta cuando me ayudas a entender. ¿Hay alguna imagen que me puedas describir?',
        'Creo que lo entiendo mejor ahora. ¿Podemos practicar juntos?',
        'A veces me confundo, pero contigo es más fácil aprender.',
        '¡Genial! Me gusta aprender cosas nuevas. ¿Qué más puedes enseñarme?'
      ],
      Josefina: [
        'Eso tiene sentido. ¿Podrías darme un ejemplo de la vida real?',
        'Me gusta como lo explicas. ¿Hay algo parecido en música o deportes?',
        'Creo que ya lo entiendo mejor. ¿Podemos ver otro ejemplo?',
        'Gracias por tu paciencia. A veces necesito tiempo para procesar.',
        '¡Interesante! ¿Cómo se relaciona esto con lo que me gusta?'
      ]
    };

    const randomResponse = responses[character][Math.floor(Math.random() * responses[character].length)];
    
    const response: Message = {
      id: Date.now().toString(),
      content: randomResponse,
      sender: 'character',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, response]);
    setIsTyping(false);
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    
    await simulateCharacterResponse(inputValue);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleRestart = () => {
    setMessages([]);
    const greeting: Message = {
      id: Date.now().toString(),
      content: characterInfo[character].greeting,
      sender: 'character',
      timestamp: new Date()
    };
    setMessages([greeting]);
  };

  const handleGenerateReport = () => {
    const score = Math.floor(Math.random() * 30) + 70; // Random score between 70-100
    alert(`Reporte generado\n\nPuntuación: ${score}/100\n\nEste reporte incluye:\n- Análisis de comprensión\n- Interacción educativa\n- Progreso en el diálogo\n\n¡Excelente trabajo!`);
  };

  const info = characterInfo[character];

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-[#E3F2FD] via-[#BBDEFB] to-[#90CAF9]">
      {/* Header */}
      <div className="bg-white/90 backdrop-blur-sm border-b border-blue-200 px-4 py-4 mt-16">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={onBack}
              className="p-2 hover:bg-blue-50 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-6 h-6 text-[#1E88E5]" />
            </button>
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-gradient-to-br from-[#42A5F5] to-[#90CAF9] rounded-full flex items-center justify-center">
                <span className="text-2xl">{info.emoji}</span>
              </div>
              <div>
                <h2 className="text-xl font-bold text-[#0D47A1]">{character}</h2>
                <p className="text-sm text-[#37474F]">{info.age} años - {info.grade}</p>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={handleRestart}
              className="p-2 bg-[#42A5F5] hover:bg-blue-500 text-white rounded-lg transition-colors"
              title="Reiniciar conversación"
            >
              <RotateCcw className="w-5 h-5" />
            </button>
            <button
              onClick={handleGenerateReport}
              className="p-2 bg-[#43A047] hover:bg-green-600 text-white rounded-lg transition-colors"
              title="Generar reporte"
            >
              <FileText className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[70%] px-4 py-3 rounded-2xl ${
                  message.sender === 'user'
                    ? 'bg-[#1E88E5] text-white rounded-br-sm'
                    : 'bg-white text-[#0D47A1] rounded-bl-sm shadow-sm'
                }`}
              >
                <p className="text-sm leading-relaxed">{message.content}</p>
                <span className={`text-xs mt-1 block ${
                  message.sender === 'user' ? 'text-blue-100' : 'text-[#37474F]'
                }`}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-white px-4 py-3 rounded-2xl rounded-bl-sm shadow-sm">
                <div className="flex items-center space-x-2">
                  <Loader className="w-4 h-4 animate-spin text-[#1E88E5]" />
                  <span className="text-[#37474F] text-sm">
                    {character} está escribiendo...
                  </span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Message Input */}
      <div className="bg-white/90 backdrop-blur-sm border-t border-blue-200 px-4 py-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-end space-x-3">
            <div className="flex-1">
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={`Escribe un mensaje a ${character}...`}
                className="w-full px-4 py-3 border border-blue-200 rounded-2xl focus:ring-2 focus:ring-[#1E88E5] focus:border-transparent outline-none resize-none transition-all"
                disabled={isTyping}
              />
            </div>
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isTyping}
              className="p-3 bg-[#1E88E5] hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-2xl transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;