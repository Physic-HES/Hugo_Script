function [errorCode, Type] = GatheringExternalConfigurationGet(socketId)
%GatheringExternalConfigurationGet :  Read different mnemonique type
%
%	[errorCode, Type] = GatheringExternalConfigurationGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring Type


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
Type = '';
for i = 1:6554
	Type = [Type '          '];
end

% lib call
[errorCode, Type] = calllib('XPS_Q8_drivers', 'GatheringExternalConfigurationGet', socketId, Type);
