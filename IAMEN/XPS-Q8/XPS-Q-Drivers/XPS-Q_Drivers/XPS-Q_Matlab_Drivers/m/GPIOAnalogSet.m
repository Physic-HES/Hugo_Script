function [errorCode] = GPIOAnalogSet(socketId, GPIOName, AnalogOutputValue)
%GPIOAnalogSet :  Set analog output for one or few output
%
%	[errorCode] = GPIOAnalogSet(socketId, GPIOName, AnalogOutputValue)
%
%	* Input parameters :
%		int32 socketId
%		cstring GPIOName
%		double AnalogOutputValue
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Count the number of element in the API
[temp, iMax] = size(GPIOName);
i = 1;
nbElement = 0;
while (i < iMax)
	if (GPIOName(i) == ' ')
		nbElement = nbElement + 1;
		while (i < iMax & GPIOName(i) == ' ')
			i = i + 1;
		end
	end
	if (i == (iMax-1) & GPIOName(i) ~= ' ')
		nbElement = nbElement + 1;
	end
	i = i + 1;
end

% lib call
[errorCode, GPIOName] = calllib('XPS_Q8_drivers', 'GPIOAnalogSet', socketId, nbElement, GPIOName, AnalogOutputValue);
