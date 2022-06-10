function [errorCode] = EventExtendedConfigurationTriggerSet(socketId, ExtendedEventName, EventParameter1, EventParameter2, EventParameter3, EventParameter4)
%EventExtendedConfigurationTriggerSet :  Configure one or several events
%
%	[errorCode] = EventExtendedConfigurationTriggerSet(socketId, ExtendedEventName, EventParameter1, EventParameter2, EventParameter3, EventParameter4)
%
%	* Input parameters :
%		int32 socketId
%		cstring ExtendedEventName
%		cstring EventParameter1
%		cstring EventParameter2
%		cstring EventParameter3
%		cstring EventParameter4
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Count the number of element in the API
[temp, iMax] = size(ExtendedEventName);
i = 1;
nbElement = 0;
while (i < iMax)
	if (ExtendedEventName(i) == ' ')
		nbElement = nbElement + 1;
		while (i < iMax & ExtendedEventName(i) == ' ')
			i = i + 1;
		end
	end
	if (i == (iMax-1) & ExtendedEventName(i) ~= ' ')
		nbElement = nbElement + 1;
	end
	i = i + 1;
end

% lib call
[errorCode, ExtendedEventName, EventParameter1, EventParameter2, EventParameter3, EventParameter4] = calllib('XPS_Q8_drivers', 'EventExtendedConfigurationTriggerSet', socketId, nbElement, ExtendedEventName, EventParameter1, EventParameter2, EventParameter3, EventParameter4);
