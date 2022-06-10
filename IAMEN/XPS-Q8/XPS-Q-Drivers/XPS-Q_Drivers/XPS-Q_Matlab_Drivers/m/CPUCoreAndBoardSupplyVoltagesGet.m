function [errorCode, VoltageCPUCore, SupplyVoltage1P5V, SupplyVoltage3P3V, SupplyVoltage5V, SupplyVoltage12V, SupplyVoltageM12V, SupplyVoltageM5V, SupplyVoltage5VSB] = CPUCoreAndBoardSupplyVoltagesGet(socketId)
%CPUCoreAndBoardSupplyVoltagesGet :  Get raw encoder positions for single axis theta encoder
%
%	[errorCode, VoltageCPUCore, SupplyVoltage1P5V, SupplyVoltage3P3V, SupplyVoltage5V, SupplyVoltage12V, SupplyVoltageM12V, SupplyVoltageM5V, SupplyVoltage5VSB] = CPUCoreAndBoardSupplyVoltagesGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		doublePtr VoltageCPUCore
%		doublePtr SupplyVoltage1P5V
%		doublePtr SupplyVoltage3P3V
%		doublePtr SupplyVoltage5V
%		doublePtr SupplyVoltage12V
%		doublePtr SupplyVoltageM12V
%		doublePtr SupplyVoltageM5V
%		doublePtr SupplyVoltage5VSB


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
VoltageCPUCore = 0;
SupplyVoltage1P5V = 0;
SupplyVoltage3P3V = 0;
SupplyVoltage5V = 0;
SupplyVoltage12V = 0;
SupplyVoltageM12V = 0;
SupplyVoltageM5V = 0;
SupplyVoltage5VSB = 0;

% lib call
[errorCode, VoltageCPUCore, SupplyVoltage1P5V, SupplyVoltage3P3V, SupplyVoltage5V, SupplyVoltage12V, SupplyVoltageM12V, SupplyVoltageM5V, SupplyVoltage5VSB] = calllib('XPS_Q8_drivers', 'CPUCoreAndBoardSupplyVoltagesGet', socketId, VoltageCPUCore, SupplyVoltage1P5V, SupplyVoltage3P3V, SupplyVoltage5V, SupplyVoltage12V, SupplyVoltageM12V, SupplyVoltageM5V, SupplyVoltage5VSB);
