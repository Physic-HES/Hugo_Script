function [errorCode, ActionConfiguration] = EventExtendedConfigurationActionGet(socketId)
%EventExtendedConfigurationActionGet :  Read the action configuration
%
%	[errorCode, ActionConfiguration] = EventExtendedConfigurationActionGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring ActionConfiguration


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
ActionConfiguration = '';
for i = 1:205
	ActionConfiguration = [ActionConfiguration '          '];
end

% lib call
[errorCode, ActionConfiguration] = calllib('XPS_Q8_drivers', 'EventExtendedConfigurationActionGet', socketId, ActionConfiguration);
