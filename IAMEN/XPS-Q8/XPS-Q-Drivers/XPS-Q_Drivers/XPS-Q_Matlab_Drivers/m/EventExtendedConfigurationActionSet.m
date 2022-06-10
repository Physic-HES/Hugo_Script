function [errorCode] = EventExtendedConfigurationActionSet(socketId, ExtendedActionName, ActionParameter1, ActionParameter2, ActionParameter3, ActionParameter4)
%EventExtendedConfigurationActionSet :  Configure one or several actions
%
%	[errorCode] = EventExtendedConfigurationActionSet(socketId, ExtendedActionName, ActionParameter1, ActionParameter2, ActionParameter3, ActionParameter4)
%
%	* Input parameters :
%		int32 socketId
%		cstring ExtendedActionName
%		cstring ActionParameter1
%		cstring ActionParameter2
%		cstring ActionParameter3
%		cstring ActionParameter4
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Count the number of element in the API
[temp, iMax] = size(ExtendedActionName);
i = 1;
nbElement = 0;
while (i < iMax)
	if (ExtendedActionName(i) == ' ')
		nbElement = nbElement + 1;
		while (i < iMax & ExtendedActionName(i) == ' ')
			i = i + 1;
		end
	end
	if (i == (iMax-1) & ExtendedActionName(i) ~= ' ')
		nbElement = nbElement + 1;
	end
	i = i + 1;
end

% lib call
[errorCode, ExtendedActionName, ActionParameter1, ActionParameter2, ActionParameter3, ActionParameter4] = calllib('XPS_Q8_drivers', 'EventExtendedConfigurationActionSet', socketId, nbElement, ExtendedActionName, ActionParameter1, ActionParameter2, ActionParameter3, ActionParameter4);
