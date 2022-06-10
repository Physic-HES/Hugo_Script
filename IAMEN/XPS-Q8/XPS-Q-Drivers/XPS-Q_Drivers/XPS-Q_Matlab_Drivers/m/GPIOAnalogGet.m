function [errorCode, AnalogValue] = GPIOAnalogGet(socketId, GPIOName)
%GPIOAnalogGet :  Read analog input or analog output for one or few input
%
%	[errorCode, AnalogValue] = GPIOAnalogGet(socketId, GPIOName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GPIOName
%	* Output parameters :
%		int32 errorCode
%		doublePtr AnalogValue


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Count the number of element in the API
[temp, iMax] = size(GPIOName);
i = 1;
nbElement = 0;
AnalogValue = [];
while (i < iMax)
	if (GPIOName(i) == ' ')
		nbElement = nbElement + 1;
		AnalogValue = [AnalogValue 0];
		while (i < iMax & GPIOName(i) == ' ')
			i = i + 1;
		end
	end
	if (i == (iMax-1) & GPIOName(i) ~= ' ')
		nbElement = nbElement + 1;
		AnalogValue = [AnalogValue 0];
	end
	i = i + 1;
end

% lib call
[errorCode, GPIOName, AnalogValue] = calllib('XPS_Q8_drivers', 'GPIOAnalogGet', socketId, nbElement, GPIOName, AnalogValue);
